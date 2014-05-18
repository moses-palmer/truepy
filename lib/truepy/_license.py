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
import gzip
import hashlib
import io
import OpenSSL
import sys

from Crypto.Cipher import DES

from . import LicenseData, fromstring
from ._bean import deserialize, serialize, to_document
from ._bean_serializers import bean_class


@bean_class('de.schlichtherle.xml.GenericCertificate')
class License(object):
    """
    A class representing a signed license.
    """

    SIGNATURE_ENCODING = 'US-ASCII/Base64'

    SALT = b'\xCE\xFB\xDE\xAC\x05\x02\x19\x71'
    ITERATIONS = 2005
    DIGEST = hashlib.md5
    KEY_SIZE = 8

    BLOCK_SIZE = 8

    class InvalidSignatureException(Exception):
        """Raised when the signature does not match"""
        pass

    class InvalidPasswordException(Exception):
        """Raised when the license password is invalid"""
        pass

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
        self.data = deserialize(license_data_xml[0])
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

    def verify(self, certificate):
        """
        Verifies the signature of this certificate against a certificate.

        @param certificate
            The issuer certificate.
        @raise truepy.License.InvalidSignatureException if the signature does
            not match
        """
        try:
            OpenSSL.crypto.verify(
                certificate,
                base64.b64decode(self.signature),
                self.encoded.encode('ascii'),
                self._signature_digest)
        except Exception as e:
            raise self.InvalidSignatureException(e)

    @classmethod
    def _key_iv(self, password, salt = SALT, iterations = ITERATIONS,
            digest = hashlib.md5, key_size = KEY_SIZE):
        """
        Derives a key from a password.

        The default values will generate a key and IV for DES encryption
        compatible with PKCS#5 1.5.

        @param password
            The password from which to derive the key.
        @param salt
            The password salt. This parameter is not validated.
        @param iteration
            The number of hashing iterations. This parameter is not validated.
        @param digest
            The digest method to use.
        @param key_size
            The key size to generate.
        @return the tuple (key, iv)
        """
        # Perform the hashing iterations
        keyiv = password + salt
        for i in range(iterations):
            keyiv = digest(keyiv).digest()

        return (keyiv[:key_size], keyiv[key_size:])

    @classmethod
    def _unpad(self, data):
        """
        Removes PKCS#5 padding from data.

        @param data
            The data to unpad.
        @raise truepy.License.InvalidPasswordException if the padding is
            invalid
        """
        if sys.version_info.major < 3:
            padding_length = ord(data[-1])
            is_valid = all(ord(d) == padding_length
                for d in data[-padding_length:])
        else:
            padding_length = data[-1]
            is_valid = all(d == padding_length
                for d in data[-padding_length:])
        if not is_valid:
            raise self.InvalidPasswordException('invalid PKCS#5 padding')

        return data[:-padding_length]

    @classmethod
    def _pad(self, data, block_size = BLOCK_SIZE):
        """
        Adds PKCS#5 padding to data.

        @param data
            The data to pad.
        @param block_size
            The encryption block size. The default value is compatible with DES.
        @return padded data
        """
        padding_length = block_size - len(data) % block_size

        if sys.version_info.major < 3:
            return data + ''.join(
                [chr(block_size - len(data) % block_size)] * padding_length)
        else:
            return data + bytes(padding_length
                for i in range(block_size - len(data) % block_size))

    @classmethod
    def load(self, f, password):
        """
        Loads a license from a stream.

        @param f
            The data stream.
        @param password
            The password used by the licensed application.
        @return a License object
        @raise ValueError if the input data is invalid
        @raise truepy.License.InvalidPasswordException if the password is
            invalid
        """
        # Initialise cryptography
        key, iv = self._key_iv(password)
        des = DES.new(
            key = key,
            IV = iv,
            mode = DES.MODE_CBC)

        # Decrypt the input stream
        encrypted_data = f.read()
        decrypted_data = self._unpad(des.decrypt(encrypted_data))

        # Decompress and parse the XML
        decrypted_stream = io.BytesIO(decrypted_data)
        with gzip.GzipFile(fileobj = decrypted_stream, mode = 'r') as gz:
            xml_data = gz.read()

        # Use the first child of the top-level java element
        element = fromstring(xml_data)[0]
        return deserialize(element)

    def store(self, f, password):
        """
        Stores this license to a stream.

        @param f
            The data stream.
        @param password
            The password used by the license application.
        """
        # Initialise cryptography
        key, iv = self._key_iv(password)
        des = DES.new(
            key = key,
            IV = iv,
            mode = DES.MODE_CBC)

        # Serialize the license
        xml_data = to_document(serialize(self)) if sys.version_info.major < 3 \
            else bytes(to_document(serialize(self)), 'ascii')

        # Compress the XML
        compressed_stream = io.BytesIO()
        with gzip.GzipFile(fileobj = compressed_stream, mode = 'w') as gz:
            gz.write(xml_data)
        compressed_data = compressed_stream.getvalue()

        # Encrypt the data and write it to the output stream
        encrypted_data = des.encrypt(self._pad(compressed_data))
        f.write(encrypted_data)
