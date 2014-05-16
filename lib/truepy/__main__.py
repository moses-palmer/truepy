# coding=utf-8
'''
truepy
Copyright (C) 2014 Moses Palmér

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
'''

import OpenSSL


def main(**args):
    # TODO: Implement
    return 0


import argparse
import getpass
import sys


class PasswordAction(argparse.Action):
    def __call__(self, parser, namespace, value, option_string = None):
        password = value[-1] if isinstance(value, list) else value
        destination = ' '.join(s
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
    def __call__(self, parser, namespace, value, option_string = None):
        with open(value, 'rb') as f:
            data = f.read()
        certificate = None
        for file_type in (
                OpenSSL.crypto.FILETYPE_PEM,
                OpenSSL.crypto.FILETYPE_ASN1):
            try:
                certificate = OpenSSL.crypto.load_certificate(
                    file_type, data)
                break
            except:
                pass
        if certificate is None:
            raise argparse.ArgumentError(self,
                'Failed to load certificate')
        else:
            setattr(namespace, self.dest, certificate)


class KeyAction(PasswordAction):
    def get_value(self, value, password):
        with open(value[0], 'rb') as f:
            data = f.read()
        key = None
        for file_type in (
                OpenSSL.crypto.FILETYPE_PEM,
                OpenSSL.crypto.FILETYPE_ASN1):
            try:
                return OpenSSL.crypto.load_privatekey(file_type, data, password)
            except:
                pass
        raise argparse.ArgumentError(self,
            'Failed to load key')


parser = argparse.ArgumentParser(prog = 'truepy', description =
    'Creates and verifies TrueLicense version 1 licenses')

parser.add_argument('--issuer-certificate', help =
    'The issuer certificate.',
    action = CertificateAction)

parser.add_argument('--issuer-key', help =
    'The private key to the certificate and the password; pass "-" as password '
    'to read it from stdin.',
    nargs = 2,
    const = None,
    action = KeyAction)

parser.add_argument('--license-file-password', help =
    'The password of the license file; pass "-" to read from stdin.',
    const = None,
    action = PasswordAction)

try:
    sys.exit(main(**vars(parser.parse_args())))
except Exception as e:
    try:
        sys.stderr.write('%s\n' % e.args[0] % e.args[1:])
    except:
        sys.stderr.write('%s\n' % str(e))
    sys.exit(1)
