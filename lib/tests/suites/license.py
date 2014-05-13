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

from .. import *

import OpenSSL

from truepy import LicenseData, License
from truepy._bean import serialize, to_document


CERTIFICATE = r'''-----BEGIN CERTIFICATE-----
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
-----END CERTIFICATE-----'''
def certificate():
    return OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM,
        CERTIFICATE)

KEY = r'''-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIFDjBABgkqhkiG9w0BBQ0wMzAbBgkqhkiG9w0BBQwwDgQIlhgdHbcx56QCAggA
MBQGCCqGSIb3DQMHBAgl6ynGQoUxNQSCBMh24HR44SbY5y5U8f1NhBntEhM4XneA
zfoffsTsmzkT9MKKGTmoVmlOxQxXn6aW/QLgn+u/lp6ol3onJpCqj5ABfHc1K6iJ
a27XmJCNq9EnYjXTXjd4WnnKNJMRFjkHtTGNBhQsHX7Ua+yISgzHJ5ZEZJFh6g1U
RgrE9nNj2BaLrxYYVlg0yazom8+PMgAotNKMGg7aAz9WxrjKWa5xirhgae/9noec
/hpKobfxEamHAvUFx5JJbQdTZQvrJfBnzqy7T1y5C0mr6bDsaBGH4a5juCiykPae
tTfCXCqKwAclRBGdYDgKz4HY74e5Jjctixj8jZCQnxqvT1RhU9oGZYv3lteXQLQX
uWibW+cEt/boeC52f84AEqMo0C9SVANILyikQWSRP+9AlkTFhvWkKUqmir++VfUd
1qXNqu1LxWXV8d6MeIYxE7gxYiBjDot8uicsGMHkArd5g7zMGVQ7ZervVJ6gdBSG
IwQDdGdAQPv6v+BE9x1SM/nSJ/VCQeLEHp8x/XvoSMHICCfUnh1GztfUBcVSN478
GCIi2xiOGCmmz3jwdgAWp1ybnX6/O+ouKd1FXz0GrlYTVlhaIGw/MX9hMDeft4KM
qEz/gGNLXtvN84sNVLSmnrs4dWlyPp4B5bDX7H+Hzxepnaf3C18oR7a8LLEkJ8S0
NTnXz1y5YjZGXv1oWfi4fQFFrGXIyNgJ9dbZK2pLSk+nurddarYc+j19DpzXdbrD
R2pBBautzfXONqbbExq5ce28fAk/fw5ZzgtEj8KuR3h7SKm1DqW4Yl0Tj2asCn9W
yAtJXvpVOeGNu8fPAw2gvibXTyk+MFmCNYKvwP3ZK8AHrVi3WMk56wzs86gI3G8j
ELzaf1xKCTDUdPuBwAfu8+FoakjzhIxH589Ec+G/Wl9mMes8DuNHbuob+g72ioMh
i6T4STKF2MzARyM4TzHZCE/lGigDBnHHeL6bTZihIQApIGrsLPYPfG9BYQCBhUOM
8BL5m6+cO57z9AOgCpmUqUonN9kbzv11TJ2St1Zd7fsmuuap+p4aP4QrDSPvEueI
xaQDUxS3eCynvJdcxnwncz2C4FLgQ4Viz3IqSE7l5rJcVVfunOyhuFEEEh4y8LCJ
8iVFxLFLfnvhHLMR/7aIU3nmyRH6Vhu3pZn+DPKJqofuAVJCTgQptbGhyJFVN1Zp
HO2RlJrm8mqq1Wa06RwyZ55cY3InIW3Dz5GNh2NXqAWN11nSeeH3X2b1wI7+ocTJ
nSLBsufMnd1WV/CRUBWlc0dJLeeeoonTZCXW3ztaGRqTGKGsakA+HReDuNbV9BO5
oRR2Iu3vVrKweb20YDyzOKi/D+yYkXlf8fVStzxGP1zgXGj071UKwdBx38d1ufKA
mxoxY3YIIyTClvGEEfMr6LRkEkr0CV1d2cNRRO80APOWG12C9HkjzM3DDWAJTqPF
noVwDJXDTWI2AEO7CpooVRiiJHiKbiGy6NeABT9hrnI1CloYNSWzH0jSnv4uTQNT
LuJDP6cJjoDJ7B9V4GyFOnaFpoBXxyJw0kcfC/nenApJomVGvusCxGDuDeS0yoIe
fhvM5+bpSfzm6IhDaKRkh/wzfbKzjPCAULUIZX5jfIOG9RrThYQqPy9RokbFr3Im
k9A=
-----END ENCRYPTED PRIVATE KEY-----'''
PASSWORD = b'SecretPassword'
def key():
    return OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM,
        KEY, PASSWORD)


@test
def License_encoded0():
    """Tests that License() with invalid encoded data raises ValueError"""
    with assert_exception(ValueError):
        License(
            '<invalid/>',
            '<signature>')


@test
def License_encoded1():
    """Tests that License() with valid encoded data has correct encoded value"""
    License(
        to_document(serialize(
            LicenseData('2014-01-01T00:00:00', '2014-01-01T00:00:01'))),
        '<signature>')


@test
def License_signature_algorithm0():
    """Tests License() for invalid signature_algorithm"""
    with assert_exception(ValueError):
        License(to_document(serialize(
            LicenseData('2014-01-01T00:00:00', '2014-01-01T00:00:01'))),
        '<signature>',
        signature_algorithm = 'invalid')


@test
def License_signature_algorithm1():
    """Tests License() for valid, non-default signature_algorithm"""
    License(to_document(serialize(
        LicenseData('2014-01-01T00:00:00', '2014-01-01T00:00:01'))),
    '<signature>',
    signature_algorithm = 'HELLOwithWORLD')


@test
def License_signature_encoding0():
    """Tests License() for invalid signature_encoding"""
    with assert_exception(ValueError):
        License(to_document(serialize(
            LicenseData('2014-01-01T00:00:00', '2014-01-01T00:00:01'))),
        '<signature>',
        signature_encoding = 'UTF-8/Base64')


@test
def License_issue_invalid_license_data():
    """Tests that License.issue with invalid license_data fails"""
    with assert_exception(ValueError):
        License.issue(certificate(), key(),
            license_data = None)
    with assert_exception(ValueError):
        License.issue(certificate(), key(),
            license_data = LicenseData(
                '2014-01-01T00:00:00',
                '2014-01-01T00:00:01'),
            not_before = '2014-01-01T00:00:00')
    with assert_exception(ValueError):
        License.issue(certificate(), key(),
            license_data = LicenseData(
                '2014-01-01T00:00:00',
                '2014-01-01T00:00:01'),
            issuer = 'CN=must not be passed')
    with assert_exception(ValueError):
        License.issue(certificate(), key(),
            not_before = '2014-01-01T00:00:00')

@test
def License_issue_valid():
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
        'bHteI3Cuc38CRVYw+DeBOYDtW8iGrnZnCQ4K1YC3O2o9vHTWwHd3CDRj2dVT17ox5TQcwT'
        'K0QOcbtJVDOaBxTln+7K5TW0iujOaroQivQEoIPyq4ExzphhcoNSIHnVlm4uL81/ZKnWzi'
        'nvDHcKAzwTppIIybhV0fivCQkUa+HIKgQ0GvCfph9fL+krJ9KW/LH8Z7JUpOO9b1BgZ9ai'
        'JxnrJy13QillegpHOTaRSL2JvGs1smIyW4+gLFle4y0uj8LdScBcqHctkVQRuathgylOxl'
        'QsOdDEM5c9shmWFgWmeQi+XpiZhE5kXt1oisrXXJ+bMbQ5nuFHT/SMFwLQ0JXg==')

    assert_eq(
        expected,
        License.issue(certificate(), key(),
            license_data = LicenseData(
                '2014-01-01T00:00:00',
                '2014-01-01T00:00:01')).signature)
