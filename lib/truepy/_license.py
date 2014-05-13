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

import base64
import OpenSSL
import sys

from . import LicenseData, fromstring
from ._bean import deserialize, serialize, to_document


class License(object):
    """
    A class representing a signed license.
    """

    SIGNATURE_ENCODING = 'US-ASCII/Base64'

    @property
    def encoded(self):
        """The encoded license data"""
        return self._encoded

    @property
    def signature(self):
        """The signature of the license data as base 64 encoded data"""
        return self._signature

    @property
    def signature_algorithm(self):
        """The signature algorithm used to sign"""
        return '%swith%s' % (self._signature_digest, self._signature_encryption)

    @property
    def signature_encoding(self):
        """The encoding of the signature; this is always US-ASCII/Base64"""
        return 'US-ASCII/Base64'

    @signature_encoding.setter
    def signature_encoding(self, value):
        if value != self.SIGNATURE_ENCODING:
            raise ValueError('invalid signature encoding: %s', value)

    def __init__(self, encoded, signature, signature_algorithm = 'SHA1withRSA',
            signature_encoding = SIGNATURE_ENCODING):
        """
        Creates a new license object.

        @param encoded
            The encoded license data.
        @param signature
            The license signature.
        @param signature_algorithm
            The algorithm used to sign the license. This must be on the form
            <digest>with<encryption>.
        @param signature_encoding
            The encoding of the signature. This must be US-ASCII/Base64.
        @raise ValueError if encoded is not an encoded LicenseData object, if
            signature_algorithm is invalid or if signature_encoding is not
            US-ASCII/Base64
        """
        license_data_xml = fromstring(encoded)
        if license_data_xml.tag != 'java' or len(license_data_xml) != 1:
            raise ValueError('invalid encoded license data: %s', encoded)
        self._license_data = deserialize(license_data_xml[0])
        self._encoded = encoded

        self._signature = signature
        try:
            self._signature_digest, self._signature_encryption = \
                signature_algorithm.split('with')
        except ValueError:
            raise ValueError('invalid signature algorithm: %s',
                signature_algorithm)
        self.signature_encoding = signature_encoding

    @classmethod
    def issue(self, certificate, key, digest = 'SHA1', **license_data):
        """
        Issues a new License.

        @param certificate
            The issuer certificate.
        @param key
            The private key of the certificate.
        @param digest
            The digest algorithm to use.
        @param license_data
            Parameter to pass on to truepy.LicenseData. Do not pass issuer; this
            value will be read from the certificate subject. You may also
            specify the single value license_data; this must in that case be an
            instance of truepy.LicenseData
        @raise ValueError if license data cannot be created from the keyword
            arguments or if the issuer name is passed
        """
        if 'license_data' in license_data:
            if len(license_data) != 1:
                raise ValueError('invalid keyword arguments')
            license_data = license_data['license_data']
        else:
            if 'issuer' in license_data:
                raise ValueError('issuer must not be passed')
            license_data['issuer'] = ','.join('='.join(
                    str(part, 'ascii') if sys.version_info.major > 2
                    else part for part in parts)
                for parts in certificate.get_subject().get_components())
            try:
                license_data = LicenseData(**license_data)
            except TypeError:
                raise ValueError('invalid keyword arguments')
        if not isinstance(license_data, LicenseData):
            raise ValueError('invalid license_data: %s', license_data)

        encoded = to_document(serialize(license_data))

        if key.type() == OpenSSL.crypto.TYPE_RSA:
            encryption = 'RSA'
        elif key.type() == OpenSSL.crypto.TYPE_DSA:
            encryption = 'DSA'
        else:
            raise ValueError('unknown key type')

        signature = base64.b64encode(OpenSSL.crypto.sign(
            key,
            encoded.encode('ascii'),
            digest)).decode('ascii')

        signature_algorithm = 'with'.join((digest, encryption))

        return License(encoded, signature, signature_algorithm)
