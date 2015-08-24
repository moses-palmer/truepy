# coding: utf-8
# truepy
# Copyright (C) 2014-2015 Moses Palmér
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

import unittest

import cryptography.hazmat.backends as backends
import cryptography.x509

from truepy import Name, tostring
from truepy._bean import serialize


class NameTest(unittest.TestCase):
    @property
    def certificate(self):
        CERTIFICATE = b'\n'.join(
            line.strip()
            for line in b'''
            -----BEGIN CERTIFICATE-----
            MIIDuTCCAqGgAwIBAgIJAKSXrdRuO5qWMA0GCSqGSIb3DQEBCwUAMHMxCzAJBgNV
            BAYTAlhYMRMwEQYDVQQIDApTb21lLVN0YXRlMRQwEgYDVQQHDAtNYWRldXB2aWxs
            ZTEhMB8GA1UECgwYSW50ZXJuZXQgV2lkZ2l0cyBQdHkgTHRkMRYwFAYDVQQLDA1M
            b2FmaW5nIGRlcHQuMB4XDTE0MDUxMjA3MDk0M1oXDTQxMDkyNzA3MDk0M1owczEL
            MAkGA1UEBhMCWFgxEzARBgNVBAgMClNvbWUtU3RhdGUxFDASBgNVBAcMC01hZGV1
            cHZpbGxlMSEwHwYDVQQKDBhJbnRlcm5ldCBXaWRnaXRzIFB0eSBMdGQxFjAUBgNV
            BAsMDUxvYWZpbmcgZGVwdC4wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIB
            AQDV1Y9uDboYcKbPxyQ6zQOqCrIO9omiXd9zhem8U+RANrgmC5wuImwsJkt5jovA
            pD1Qyw24gZrQxag2jn1KV1x8TBPz4iE7LWQ3MGbpw19aOJyiynLcu7AKwAN5TLi6
            GVnoQOWCVRmXzc3aQo7YeF2pIBPdS1zTm52FWKQG8P+019rdwDNEgFpl3NJw+75O
            iDwPoskzGiF5IvjWrzdbU9DcE3T8wMw11XyT6SCACmkjWB1DTLugvLvVX3crfVMs
            jdcWBEywp46UyyioZWKG/oTSawfYqZXBMGWKCkhK/R/gEQ3bdY9I/9hEasQ+6nE8
            WHwBS0Ilci4w9whE8v/00nefAgMBAAGjUDBOMB0GA1UdDgQWBBTH8td6Ja9k3OpQ
            mbM3prSOummUIzAfBgNVHSMEGDAWgBTH8td6Ja9k3OpQmbM3prSOummUIzAMBgNV
            HRMEBTADAQH/MA0GCSqGSIb3DQEBCwUAA4IBAQB0ZM38ACp+/y+PvQSQk/BSXkfs
            L5DjoTj/YPGprs09gF1QRF5oxsrT8aS5E5jrn2GRWCq1jjEx+uH+w/6c1tF6El18
            N6RlgNJLctC7fDTAOuoFk8OXeNJ1vN24t4JqLN06FS62eL1s+LQMaThto2oXNicn
            94ywFwXRjI1ChWUbFqvJQ4ycMyBABujXkm5VtVbzXyfJL+FfqhJhljqNfvXeCWbO
            9O8AWMLa8JqUjGO3Cej4nfVbkKhLE+xg/18K4WAAsq154wCe0sr2MlwR8k/cLlCL
            jpLCDa3fceUjfLs1utsf8iG6Iwbol1imGqzqyt1zA4H7l+QPgANqJ+Er9i5K
            -----END CERTIFICATE-----'''.splitlines()
            if line.strip())
        return cryptography.x509.load_pem_x509_certificate(
            CERTIFICATE,
            backends.default_backend())

    def test_escape_no_escape(self):
        """Tests that Name.escape for string not needing escaping returns the
        input string"""
        s = 'hello world'
        expected = s

        self.assertEqual(
            expected,
            Name.escape(s))

    def test_escape_with_escape(self):
        """Tests that Name.escape for string needing escaping returns the
        correct string"""
        s = 'hello, "world"; insert <token + value>'
        expected = 'hello#2C #22world#22#3B insert #3Ctoken #2B value#3E'

        self.assertEqual(
            expected,
            Name.escape(s))

    def test_unescape_no_escape(self):
        """Tests that Name.unescape for unescaped string returns the input
        string"""
        s = 'hello world'
        expected = s

        self.assertEqual(
            expected, Name.unescape(s))

    def test_unescape_with_escape(self):
        """Tests that Name.unescape for escaped string returns the correct
        string"""
        s = 'hello, "world"; insert <token + value>'

        self.assertEqual(
            s, Name.unescape(Name.escape(s)))

    def test_unescape_invalid_escape(self):
        """Tests that Name.unescape for escaped string with invalid escape seqienmce
        raises ValueError"""
        with self.assertRaises(ValueError):
            Name.unescape('#01')

    def test_valid_string(self):
        """Tests Name() from valid string returns the correct sequence"""
        self.assertEqual(
            [('CN', '<token>'), ('O', 'organisation')],
            Name('CN=#3Ctoken#3E,O=organisation'))

    def test_invalid_string(self):
        """Tests that Name() from invalid string raises ValueError"""
        with self.assertRaises(ValueError):
            Name('CN=invalid escape sequence#01')
        with self.assertRaises(ValueError):
            Name('CN=valid escape sequence, no type')

    def test_str(self):
        """Tests that str(Name()) return the input string"""
        s = 'CN=#3Ctoken#3E,O=organisation'
        self.assertEqual(
            s,
            str(Name(s)))

    def test_str_strip_space(self):
        """Tests that str(Name()) return the input string with leading and
        trailing space stripped for values"""
        s = 'CN=#3Ctoken#3E , O=organisation '
        expected = 'CN=#3Ctoken#3E,O=organisation'
        self.assertEqual(
            expected,
            str(Name(s)))

    def test_serialize(self):
        """Tests that a name can be serialised to XML"""
        s = 'CN=#3Ctoken#3E , O=organisation '

        self.assertEqual(
            '<object class="javax.security.auth.x500.X500Principal">'
            '<string>CN=#3Ctoken#3E,O=organisation</string>'
            '</object>',
            tostring(serialize(Name(s))))

    def test_create_from_list(self):
        """Tests that a name can be created from a list"""
        s = [('CN', '<token>'), ('O', 'organisation')]

        self.assertEqual(
            '<object class="javax.security.auth.x500.X500Principal">'
            '<string>CN=#3Ctoken#3E,O=organisation</string>'
            '</object>',
            tostring(serialize(Name(s))))

    def test_create_from_name(self):
        """Tests that a name can be created from a cryptography.x509.Name"""
        self.assertEqual(
            '<object class="javax.security.auth.x500.X500Principal">'
            '<string>C=XX,ST=Some-State,L=Madeupville,O=Internet Widgits Pty '
            'Ltd,OU=Loafing dept.</string>'
            '</object>',
            tostring(serialize(Name.from_x509_name(self.certificate.subject))))
