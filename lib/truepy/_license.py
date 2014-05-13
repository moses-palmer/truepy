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
        raise NotImplementedError()

    @property
    def signature_algorithm(self):
        """The signature algorithm used to sign"""
        raise NotImplementedError()

    @property
    def signature_encoding(self):
        """The encoding of the signature; this is always US-ASCII/Base64"""
        raise NotImplementedError()

    def __init__(self, encoded, signature, signature_algorithm = 'SHA1withRSA',
            signature_encoding = SIGNATURE_ENCODING):
        """
        Creates a new license object.

        @param encoded
            The encoded license data.
        @param signature
            The license signature.
        @param signature_algorithm
            The algorithm used to sign the license.
        @param signature_encoding
            The encoding of the signature. This must be US-ASCII/Base64.
        @raise ValueError if encoded is not an encoded LicenseData object
        """
        license_data_xml = fromstring(encoded)
        if license_data_xml.tag != 'java' or len(license_data_xml) != 1:
            raise ValueError('invalid encoded license data: %s', encoded)
        self._license_data = deserialize(license_data_xml[0])
        self._encoded = encoded
