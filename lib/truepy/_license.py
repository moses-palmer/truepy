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

from . import fromstring
from ._bean import deserialize


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
