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

import base64
import io
import OpenSSL

from truepy import LicenseData, License
from truepy._bean import serialize, to_document


class LicenseTest(unittest.TestCase):
    def test_encoded_invalid(self):
        """Tests that License() with invalid encoded data raises ValueError"""
        with self.assertRaises(ValueError):
            License(
                '<invalid/>',
                '<signature>')

    def test_encoded_valid(self):
        """Tests that License() with valid encoded data has correct encoded
        value"""
        License(
            to_document(serialize(
                LicenseData('2014-01-01T00:00:00', '2014-01-01T00:00:01'))),
            '<signature>')

    def test_signature_algorithm_invalid(self):
        """Tests License() for invalid signature_algorithm"""
        with self.assertRaises(ValueError):
            License(
                to_document(serialize(
                    LicenseData(
                        '2014-01-01T00:00:00',
                        '2014-01-01T00:00:01'))),
                '<signature>',
                signature_algorithm='invalid')

    def test_signature_algorithm_valid_non_default_signature_algo(self):
        """Tests License() for valid, non-default signature_algorithm"""
        License(
            to_document(serialize(
                LicenseData('2014-01-01T00:00:00', '2014-01-01T00:00:01'))),
            '<signature>',
            signature_algorithm='HELLOwithWORLD')

    def test_signature_encoding_invalid(self):
        """Tests License() for invalid signature_encoding"""
        with self.assertRaises(ValueError):
            License(
                to_document(serialize(
                    LicenseData(
                        '2014-01-01T00:00:00',
                        '2014-01-01T00:00:01'))),
                '<signature>',
                signature_encoding='UTF-8/Base64')

    def test_issue_invalid_license_data(self):
        """Tests that License.issue with invalid license_data fails"""
        with self.assertRaises(ValueError):
            License.issue(
                self.certificate,
                self.key,
                license_data=None)
        with self.assertRaises(ValueError):
            License.issue(
                self.certificate,
                self.key,
                license_data=LicenseData(
                    '2014-01-01T00:00:00',
                    '2014-01-01T00:00:01'),
                not_before='2014-01-01T00:00:00')
        with self.assertRaises(ValueError):
            License.issue(
                self.certificate,
                self.key,
                license_data=LicenseData(
                    '2014-01-01T00:00:00',
                    '2014-01-01T00:00:01'),
                issuer='CN=must not be passed')
        with self.assertRaises(ValueError):
            License.issue(
                self.certificate,
                self.key,
                not_before='2014-01-01T00:00:00')

    def test_issue_valid(self):
        """Tests that the signature is correctly constructed"""
        # Generated with command below:
        '''
        python -c 'import tests.suites.license; open("key.pem", "w") \
            .write(tests.suites.license.KEY);'
        python -c 'import sys, truepy, tests.suites.license; \
           sys.stdout.write(truepy._bean.to_document(truepy._bean.serialize( \
                truepy.LicenseData( \
                    not_before = "2014-01-01T00:00:00", \
                    not_after = "2014-01-01T00:00:01"))))' \
            | openssl sha -sign key.pem -sha1 \
            | base64
        '''
        expected = (
            'BwaJUYJTcY22EiC5x/qZQVMKGeIxAwTiIejRjrch2Q/uVoUrB1ptKRn1ffGgYs5zc'
            'agsj+7YTi8bB8nim+W+ANy93WttNrgz5hl2k75D4hGmR3EGV+f45l91RYMdTHukuK'
            'ZkA+agc/At5ByHC8Qaw4+4Jdz2e0XJMJaR3aEAYIJ/5NDVKSHD2OjpGDLEc70Qwdo'
            'rUU10B4X2URasRKHuRZTv9jVz2t4Mgk4wrJHiT/gw6sHbR1U7u7PbbnbQ8Xx/c37U'
            'L54jy9ZqM+j7yEhEXqPGW5rXvj0IQmYrODLdyVzNMUa/ReC66oERy2JZA0aaFyY8l'
            'Fr5V1yC1xT4r6yMnw==')

        self.assertEqual(
            expected,
            License.issue(
                self.certificate,
                self.key,
                license_data=LicenseData(
                    '2014-01-01T00:00:00',
                    '2014-01-01T00:00:01')).signature)

    def test_verify_invalid(self):
        """Tests that License.verify raises exception for invalid signatures"""
        with self.assertRaises(License.InvalidSignatureException):
            License.issue(
                self.certificate,
                self.key,
                license_data=LicenseData(
                    '2014-01-01T00:00:00',
                    '2014-01-01T00:00:01')).verify(self.other_certificate)

    def test_verify_valid(self):
        """Tests that License.verify does not raise exception for valid
        certificate"""
        License.issue(
            self.certificate,
            self.key,
            license_data=LicenseData(
                '2014-01-01T00:00:00',
                '2014-01-01T00:00:01')).verify(self.certificate)

    def test_load_invalid_data(self):
        """Tests that License.load fails for invalid license data"""
        with self.assertRaises(License.InvalidPasswordException):
            License.load(io.BytesIO(b'hello world!!!!!'), b'password')

    def test_load_invalid_password(self):
        """Tests that License.load fails for invalid license data"""
        with self.assertRaises(License.InvalidPasswordException):
            License.load(self.license, b'invalid password')

    def test_load(self):
        """Tests that License.load succeeds with valid license data"""
        License.load(self.license, b'valid password')

    def test_store(self):
        """Tests that a license can be loaded from the stored data"""
        f = io.BytesIO()
        License.issue(
            self.certificate,
            self.key,
            license_data=LicenseData(
                '2014-01-01T00:00:00',
                '2014-01-01T00:00:01')).store(f, b'valid password')
        License.load(io.BytesIO(f.getvalue()), b'valid password')

    @property
    def certificate(self):
        return b'\n'.join(
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

    @property
    def other_certificate(self):
        return b'\n'.join(
            line.strip()
            for line in b'''
            -----BEGIN CERTIFICATE-----
            MIIDpTCCAo2gAwIBAgIJAMkGafbVKrk8MA0GCSqGSIb3DQEBCwUAMGkxCzAJBgNV
            BAYTAlhYMRMwEQYDVQQIDApTb21lLVN0YXRlMRQwEgYDVQQHDAtNYWxpY2V2aWxs
            ZTEhMB8GA1UECgwYMW50ZXJuZXQgV2lkZ2l0cyBQdHkgTHRkMQwwCgYDVQQDDANF
            dmUwHhcNMTQwNTEzMDgzMjUxWhcNMTcwMjA2MDgzMjUxWjBpMQswCQYDVQQGEwJY
            WDETMBEGA1UECAwKU29tZS1TdGF0ZTEUMBIGA1UEBwwLTWFsaWNldmlsbGUxITAf
            BgNVBAoMGDFudGVybmV0IFdpZGdpdHMgUHR5IEx0ZDEMMAoGA1UEAwwDRXZlMIIB
            IjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA5vNPMq01miQ7NUimwpyobV5J
            MRjCw+A3OPn0lPenfWzveNjV2voYal7W6S25NT9fz9f/lKAQmCJZw8BU+Jztvrmp
            z4Fl6NgnjwC6SMKyATgobYCYnrMmVcX7y+PlMt27m11A7YBlAbwPpU8ivYHCQxIK
            mf0uM6g1g94Apy115wzhDUppsIkLVR4MYTJ8wX9yiD6Luj/ghKO8MMaMJtIQ7tO9
            FtozkLEff1VRcW+llWP/Owe9TjJwGueJxrtb+WhO3Rz24OGX/fjxXJDSAT1PqWWG
            wRuGkMffx8zhf9YvF1ubdDHJB3c/Vhqf3EKrWsdbO9CKIbJZp/QlMxcubqS35wID
            AQABo1AwTjAdBgNVHQ4EFgQUffWcdigWLmCm5KvgTlMAE67enGowHwYDVR0jBBgw
            FoAUffWcdigWLmCm5KvgTlMAE67enGowDAYDVR0TBAUwAwEB/zANBgkqhkiG9w0B
            AQsFAAOCAQEAR7/UUFuu6qlpkyVFCNFynKxW/nadJIZy5o+irRu/m2BrWKgDvtyl
            duIzBMzN/e0c22KLdBOzyeTIjDhHKC2b4C+zSRgkKJZkGYLu4GuxWVv6eU6nVPEY
            jLO1/LS1Ch2fnNnsegC4vXiQzT/4QaRhdXJSmlFO13EK1FFXo2+3btbNAtQ82AWr
            1OhdcbhCP5xHL0+paYyF5t4nsY6usCM6bJWUqf8lI7k4o3q11TrsTq6rwhA8P/9/
            +E6wUB3If+QzAyCxbEESiTt1+4OiEDK78g6JYewBOusDObiMCE14TSdMgJzJw+TW
            BSKMnCK+8l9gBOZpxrPfGQMUxyvdUpZjbg==
            -----END CERTIFICATE-----'''.splitlines()
            if line.strip())

    @property
    def key(self):
        KEY = b'\n'.join(
            line.strip()
            for line in b'''
            -----BEGIN ENCRYPTED PRIVATE KEY-----
            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
            k9A=
            -----END ENCRYPTED PRIVATE KEY-----'''.splitlines()
            if line.strip())
        PASSWORD = b'SecretPassword'
        return OpenSSL.crypto.load_privatekey(
            OpenSSL.crypto.FILETYPE_PEM,
            KEY, PASSWORD)

    @property
    def license(self):
        LICENSE = base64.b64decode(b'''
            r2dGlsYH1NaZnCjH6Gy2Lu3RicQuR0uu9el7rguz5ZE1eix3edK+lrYMeLyiVa88
            2v3rtGs1LtdyBvzP+4rcDmbzspIreKG8oGdw8E0j9bbS1ZfplIRo38+T63LLzoSi
            8kI2SAFZY9ZbCWTYhu2Vw7tPae8Kzl2nsEKze4R5+ruX/HLM6//dRs2Qbvf363Zf
            Nhpxd38V3aO1MES6qFMpY9+KoHNCgqElpui+yO3OTNz68/F+RBqAX1oy8j3k4xA1
            lVKHbKckPaHaO4Tq9D2NTEKHOyVORqlBT1Qm4wDKh4vRuEOq0S/qi3f/AwsP7E4P
            Sw+X+ICz8SjutXmiv5piQc3pRCmMgYFLsjU1TnC7ML/+Rlb5Q8RJxrRwI4/Q5Eid
            MIC4yh22Swn1uOFY/CtunHY+/nplfe3mQA8n1ms7Y/UGt8PcvTmZR2wQMKXK0Ov3
            41bRqV83EnUYl8oIwvhW4IgktctNgwZ4eIo7zuqBPxqUpvfEAyoEPGN4iEIx4DQB
            edoFIUWxqSHAeYbist21vOFYJv1s9tMzOUiAPRTD4RTifaTj/Bv8WIai28nlVxyU
            ilJmd7YbbQiU5oJCv3lXt9Nc5Ipyc4Qm+7qpiRr7Egw1OVa580HgEgwbJzfAtRem
            Cbd00+pRnsdO7ETlWUqLBF/bra/R4dfWmLbvemViTxG/UturdkvWQpbKSWkxiRoE
            gAvZhFZJeV+ZIUGxQNRjgOt0QZVAPc9K3xhpihrnV4jvdry5GFLMaPpelQ3xcrow
            Md4nio/79DpZUngR/iFY2OoGO1jJMFks9DkPs31ne6ngWLSN/lq+JZepLbS76/Et
            x+fkhc6apIgpRj3wh1F15Aw+k+s4XAsLDGDgBFFDZnlE00xw4idfAEabUok4RbVq
            A8O1IJnzwotQk9+A59ZeNETnbYAV4xmbd3XFbfVaUgimJDqdUfI9uoWsoH8tzwr3
            oM8W51XN4Zw=''')
        return io.BytesIO(LICENSE)
