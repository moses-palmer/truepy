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

import base64
import gzip
import hashlib
import io
import sys

import cryptography.x509

from Crypto.Cipher import DES

from cryptography.hazmat import backends
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dsa, padding, rsa

from . import LicenseData, fromstring
from ._bean import deserialize, serialize, to_document
from ._bean_serializers import bean_class
from ._name import Name


@bean_class('de.schlichtherle.xml.GenericCertificate')
class License(object):
    SIGNATURE_ENCODING = 'US-ASCII/Base64'

    _SALT = b'\xCE\xFB\xDE\xAC\x05\x02\x19\x71'
    _ITERATIONS = 2005
    _DIGEST = hashlib.md5
    _KEY_SIZE = 8

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
        return '%swith%s' % (
            self._signature_digest,
            self._signature_encryption)

    @property
    def signature_encoding(self):
        """The encoding of the signature; this is always *US-ASCII/Base64*"""
        return 'US-ASCII/Base64'

    @signature_encoding.setter
    def signature_encoding(self, value):
        if value != self.SIGNATURE_ENCODING:
            raise ValueError('invalid signature encoding: %s', value)

    def __init__(self, encoded, signature, signature_algorithm='SHA1withRSA',
                 signature_encoding=SIGNATURE_ENCODING):
        """A class representing a signed license.

        :param str encoded: The encoded license data.

        :param str signature: The license signature.

        :param str signature_algorithm: The algorithm used to sign the license.
            This must be on the form `<digest>with<encryption>`.

        :param str signature_encoding: The encoding of the signature. This must
            be `US-ASCII/Base64`.

        :raises ValueError: if encoded is not an encoded
            :class:`~truepy.LicenseData` object, if signature_algorithm is
            invalid or if signature_encoding is not US-ASCII/Base64
        """
        license_data_xml = fromstring(encoded)
        if license_data_xml.tag != 'java' or len(license_data_xml) != 1:
            raise ValueError('invalid encoded license data: %s', encoded)
        #: The decoded license data as an instance of
        #: :class:`~truepy.LicenseData`
        self.data = deserialize(license_data_xml[0])
        self._encoded = encoded

        self._signature = signature
        try:
            self._signature_digest, self._signature_encryption = \
                signature_algorithm.split('with')
        except ValueError:
            raise ValueError(
                'invalid signature algorithm: %s',
                signature_algorithm)
        self.signature_encoding = signature_encoding

    @classmethod
    def issue(self, certificate, key, digest='SHA1', **license_data):
        """Issues a new License.

        :param certificate: The issuer certificate.
        :type certificate: bytes or cryptography.x509.Certificate

        :param key: The private key of the certificate.

        :param str digest: The digest algorithm to use.

        :param license_data: Parameters to pass on to truepy.LicenseData. Do
            not pass issuer; this value will be read from the certificate
            subject. You may also specify the single value license_data; this
            must in that case be an instance of :class:`~truepy.LicenseData`.

        :raises ValueError: if license data cannot be created from the keyword
            arguments or if the issuer name is passed

        :return: a new license
        :rtype: truepy.License
        """
        certificate = self._certificate(certificate)

        if 'license_data' in license_data:
            if len(license_data) != 1:
                raise ValueError('invalid keyword arguments')
            license_data = license_data['license_data']
        else:
            if 'issuer' in license_data:
                raise ValueError('issuer must not be passed')
            issuer = Name.from_x509_name(certificate.subject)
            license_data['issuer'] = str(issuer)
            try:
                license_data = LicenseData(**license_data)
            except TypeError:
                raise ValueError('invalid keyword arguments')
        if not isinstance(license_data, LicenseData):
            raise ValueError('invalid license_data: %s', license_data)

        if isinstance(key, rsa.RSAPrivateKey):
            encryption = 'RSA'
        elif isinstance(key, dsa.DSAPrivateKey):
            encryption = 'DSA'
        else:
            raise ValueError('unknown key type')

        encoded = to_document(serialize(license_data))

        signer = key.signer(
            padding.PKCS1v15(),
            getattr(hashes, digest)())
        signer.update(encoded.encode('ascii'))
        signature = base64.b64encode(signer.finalize()).decode('ascii')

        return License(encoded, signature, 'with'.join((digest, encryption)))

    def _verifier(self, certificate):
        """Returns a verifier for a certificate.

        This function will attempt different factory methods, since the
        argument lists differ.

        :param cryptography.x509.Certificate certificate: The signer
            certificate.

        :return: a verifier
        """
        public_key = certificate.public_key()
        try:
            return public_key.verifier(
                base64.b64decode(self.signature),
                padding.PKCS1v15(),
                getattr(hashes, self._signature_digest)())
        except TypeError:
            return public_key.verifier(
                base64.b64decode(self.signature),
                getattr(hashes, self._signature_digest)())

    def verify(self, certificate):
        """Verifies the signature of this certificate against a certificate.

        :param certificate: The issuer certificate.
        :type certificate: bytes or cryptography.x509.Certificate

        :raises truepy.License.InvalidSignatureException: if the signature does
            not match
        """
        certificate = self._certificate(certificate)

        verifier = self._verifier(certificate)
        verifier.update(self.encoded.encode('ascii'))
        try:
            verifier.verify()
        except cryptography.exceptions.InvalidSignature as e:
            raise self.InvalidSignatureException(e)

    @classmethod
    def _certificate(self, certificate):
        """Ensures that a variable is a certificate.

        If ``certificate`` is a parsed certificate, it will be returned
        unmodified, otherwise it will be treated as a *PEM* blob.

        :param certificate: The certificate to parse.

        :return: a parsed certificate
        """
        if isinstance(certificate, cryptography.x509.Certificate):
            return certificate
        else:
            return cryptography.x509.load_pem_x509_certificate(
                certificate,
                backends.default_backend())

    @classmethod
    def _key_iv(self, password, salt=_SALT, iterations=_ITERATIONS,
                digest=_DIGEST, key_size=_KEY_SIZE):
        """Derives a key from a password.

        The default values will generate a key and IV for DES encryption
        compatible with PKCS#5 1.5.

        :param bytes password: The password from which to derive the key.

        :param bytes salt: The password salt. This parameter is not validated.

        :param int iterations: The number of hashing iterations. This parameter
            is not validated.

        :param digest: The digest method to use.

        :param int key_size: The key size to generate.

        :return: the key and IV
        :rtype: (bytes, bytes)
        """
        # Perform the hashing iterations
        keyiv = password + salt
        for i in range(iterations):
            keyiv = digest(keyiv).digest()

        return (keyiv[:key_size], keyiv[key_size:])

    @classmethod
    def _unpad(self, data):
        """ Removes PKCS#5 1.5 padding from ``data``.

        :param bytes data: The data to unpad.

        :return: unpadded data
        :rtype: bytes

        :raises truepy.License.InvalidPasswordException: if the padding is
            invalid
        """
        if sys.version_info.major < 3:
            padding_length = ord(data[-1])
            is_valid = all(
                ord(d) == padding_length
                for d in data[-padding_length:])
        else:
            padding_length = data[-1]
            is_valid = all(
                d == padding_length
                for d in data[-padding_length:])
        if not is_valid:
            raise self.InvalidPasswordException('invalid PKCS#5 padding')

        return data[:-padding_length]

    @classmethod
    def _pad(self, data, block_size=BLOCK_SIZE):
        """Adds PKCS#5 1.5 padding to ``data``.

        :param bytes data: The data to pad.

        :param int block_size: The encryption block size. The default value is
            compatible with DES.

        :return: padded data
        :rtype: bytes
        """
        padding_length = block_size - len(data) % block_size

        if sys.version_info.major < 3:
            return data + ''.join(
                [chr(block_size - len(data) % block_size)] * padding_length)
        else:
            return data + bytes(
                padding_length
                for i in range(block_size - len(data) % block_size))

    @classmethod
    def load(self, f, password):
        """Loads a license from a stream.

        :param f: The data stream.
        :type f: file or stream

        :param bytes password: The password used by the licensed application.

        :return: a license object
        :rtype: truepy.License

        :raises ValueError: if the input data is invalid
        :raises truepy.License.InvalidPasswordException: if the password is
            invalid
        """
        # Initialise cryptography
        key, iv = self._key_iv(password)
        des = DES.new(
            key=key,
            IV=iv,
            mode=DES.MODE_CBC)

        # Decrypt the input stream
        encrypted_data = f.read()
        decrypted_data = self._unpad(des.decrypt(encrypted_data))

        # Decompress and parse the XML
        decrypted_stream = io.BytesIO(decrypted_data)
        with gzip.GzipFile(fileobj=decrypted_stream, mode='r') as gz:
            xml_data = gz.read()

        # Use the first child of the top-level java element
        element = fromstring(xml_data)[0]
        return deserialize(element)

    def store(self, f, password):
        """Stores this license to a stream.

        :param f: The data stream.
        :type f: file or stream

        :param bytes password: The password used by the licensed application.
        """
        # Initialise cryptography
        key, iv = self._key_iv(password)
        des = DES.new(
            key=key,
            IV=iv,
            mode=DES.MODE_CBC)

        # Serialize the license
        xml_data = to_document(serialize(self)) if sys.version_info.major < 3 \
            else bytes(to_document(serialize(self)), 'ascii')

        # Compress the XML
        compressed_stream = io.BytesIO()
        with gzip.GzipFile(fileobj=compressed_stream, mode='w') as gz:
            gz.write(xml_data)
        compressed_data = compressed_stream.getvalue()

        # Encrypt the data and write it to the output stream
        encrypted_data = des.encrypt(self._pad(compressed_data))
        f.write(encrypted_data)
