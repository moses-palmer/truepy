# coding: utf-8
# truepy
# Copyright (C) 2014-2020 Moses Palmér
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

import argparse
import getpass
import sys

import cryptography.hazmat.primitives.serialization
import cryptography.x509

from cryptography.hazmat import backends

from . import License, LicenseData


def main(action, action_arguments, **args):
    try:
        action(*action_arguments, **args)
    except TypeError:
        raise RuntimeError(
            '%s requires additional arguments',
            action.__name__)

    return 0


ACTIONS = {}


def action(f):
    ACTIONS[f.__name__] = f
    return f


@action
def show(license_file, issuer_certificate, license_file_password, **args):
    """show [license file]
    Verifies the signature of a license file and shows information about it.
    You must specify the issuer certificate as --issuer-certificate on the
    command line, and the license file password as --license-file-password.
    """
    with open(license_file, 'rb') as f:
        try:
            license = License.load(f, license_file_password)
        except Exception as e:
            raise RuntimeError('Failed to load license file: %s', e)

    try:
        license.verify(issuer_certificate)
    except Exception as e:
        raise RuntimeError('Failed to verify license: %s', e)

    print('License information')
    print('\tissued by:\t"%s"' % str(license.data.issuer))
    print('\tissued to:\t"%s"' % str(license.data.holder))
    print('\tvalid from:\t%s' % str(license.data.not_before))
    print('\tvalid to:\t%s' % str(license.data.not_after))
    print('\tsubject:\t%s' % (
        '"%s"' % license.data.subject
        if license.data.subject
        else '<none>'))
    print('\tconsumer_type:\t%s' % (
        '"%s"' % license.data.consumer_type
        if license.data.consumer_type
        else '<none>'))
    print('\tinformation:\t%s' % (
        '"%s"' % license.data.info
        if license.data.info
        else '<none>'))
    print('\textra data:\t%s' % (
        '"%s"' % license.data.extra
        if license.data.extra
        else '<none>'))


@action
def issue(license_file, license_description, issuer_certificate, issuer_key,
          license_file_password, **args):
    """issue [license file] [license description]
    Issues a new license and shows information about it. You must specify the
    issuer certificate and key as --issuer-certificate/key on the command line,
    and the license file password as --license-file-password.

    [license description] must be one command line argument on the form
    not_before=2014-01-01T00:00:00,not_after=2016-01-01T00:00:00,... containing
    license data fields.
    """
    try:
        license_data_parameters = dict(
            (p.strip() for p in i.split('=', 1))
            for i in license_description.split(','))
    except Exception as e:
        raise RuntimeError(
            'Invalid license data description (%s): %s',
            license_description,
            e)

    try:
        license_data = LicenseData(**license_data_parameters)
    except TypeError as e:
        raise RuntimeError(
            'Incomplete license data description (%s): %s',
            license_description,
            e)

    license = License.issue(issuer_certificate, issuer_key,
                            license_data=license_data)
    with open(license_file, 'wb') as f:
        license.store(f, license_file_password)

    show(license_file, issuer_certificate, license_file_password)


class PasswordAction(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        password = value[-1] if isinstance(value, list) else value
        destination = ' '.join(
            s
            for s in self.dest.split('_')
            if not s == 'password')
        if password == '-':
            password = getpass.getpass(
                'Please enter password for %s:' % destination)
        setattr(namespace, self.dest, self.get_value(
            value[:-1] if isinstance(value, list) else [value], password))

    def get_value(self, value, password):
        return password


class CertificateAction(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        with open(value, 'rb') as f:
            data = f.read()
        certificate = None
        for file_type in (
                'pem',
                'der'):
            try:
                loader = getattr(
                    cryptography.x509,
                    'load_%s_x509_certificate' % file_type)
                certificate = loader(data, backends.default_backend())
                break
            except:
                pass
        if certificate is None:
            raise argparse.ArgumentError(
                self,
                'Failed to load certificate')
        else:
            setattr(namespace, self.dest, certificate)


class KeyAction(PasswordAction):
    def get_value(self, value, password):
        with open(value[0], 'rb') as f:
            data = f.read()
        for file_type in (
                'pem',
                'der'):
            try:
                loader = getattr(
                    cryptography.hazmat.primitives.serialization,
                    'load_%s_x509_certificate' % file_type)
                return loader(data, password, backends.default_backend())
            except:
                pass
        raise argparse.ArgumentError(
            self,
            'Failed to load key')


class ActionAction(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        try:
            action = ACTIONS[value[0]]
        except KeyError:
            raise argparse.ArgumentError(
                self,
                'Unknown action')
        setattr(namespace, self.dest, action)


parser = argparse.ArgumentParser(
    prog='truepy',
    description='Creates and verifies TrueLicense version 1 licenses',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog='Actions\n=======\n%s' % (
        '\n\n'.join(action.__doc__ for action in ACTIONS.values())))

parser.add_argument(
    '--issuer-certificate',
    help='The issuer certificate.',
    action=CertificateAction)

parser.add_argument(
    '--issuer-key',
    help='The private key to the certificate and the password; pass "-" as '
    'password to read it from stdin.',
    nargs=2,
    const=None,
    action=KeyAction)

parser.add_argument(
    '--license-file-password',
    help='The password of the license file; pass "-" to read from stdin.',
    const=None,
    action=PasswordAction)

parser.add_argument(
    '--verbose',
    help='Show a stack trace on error.',
    action='store_true')

parser.add_argument(
    'action',
    help='The action to perform; this can be any of %s' % ', '.join(
        ACTIONS.keys()),
    nargs=1,
    action=ActionAction)

parser.add_argument(
    'action_arguments',
    help='Arguments to the action. See below for more information.',
    nargs='*',
    default=[])

try:
    namespace = parser.parse_args()
    sys.exit(main(**vars(namespace)))
except Exception as e:
    try:
        sys.stderr.write('%s\n' % e.args[0] % e.args[1:])
    except:
        sys.stderr.write('%s\n' % str(e))
    if namespace and namespace.verbose:
        import traceback
        traceback.print_exc()
    sys.exit(1)
