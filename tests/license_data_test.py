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

from truepy import LicenseData, Name, fromstring, tostring
from truepy._bean import deserialize, serialize


class LicenseDataTest(unittest.TestCase):
    def test_valid_validity_window(self):
        """Test LicenseData() for valid validity window"""
        LicenseData('2014-01-01T00:00:00', '2014-01-01T00:00:01')

    def test_invalid_validity_window(self):
        """Test LicenseData() for invalid validity window"""
        with self.assertRaises(ValueError):
            LicenseData('2014-01-01T00:00:00', '2014-01-01T00:00:00')
        with self.assertRaises(ValueError):
            LicenseData('2014-01-01T00:00:01', '2014-01-01T00:00:00')

    def test_issued_unspecified(self):
        """Test LicenseData.issued for unspecified issued value"""
        license = LicenseData(
            '2014-01-01T00:00:00',
            '2014-01-01T00:00:01')
        self.assertEqual(license.issued, license.not_before)

    def test_issued_specified(self):
        """Test LicenseData.issued for specified issued value"""
        license = LicenseData(
            '2014-01-01T00:00:00',
            '2014-01-01T00:00:01',
            '2014-01-01T00:00:01')
        self.assertEqual(license.issued, license.not_after)

    def test_invalid_timestamps(self):
        """Test LicenseData() for invalid timestamps"""
        with self.assertRaises(ValueError):
            LicenseData(
                'invalid',
                '2014-01-01T00:00:01',
                '2014-01-01T00:00:03')
        with self.assertRaises(ValueError):
            LicenseData(
                '2014-01-01T00:00:00',
                'invalid',
                '2014-01-01T00:00:03')
        with self.assertRaises(ValueError):
            LicenseData(
                '2014-01-01T00:00:00',
                '2014-01-01T00:00:01',
                'invalid')

    def test_valid_issuer(self):
        """Test LicenseData() for valid issuer"""
        name = 'CN=name,O=organisation'
        expected = [('CN', 'name'), ('O', 'organisation')]
        unknown = Name(LicenseData.UNKNOWN_NAME)

        license = LicenseData(
            '2014-01-01T00:00:00',
            '2014-01-01T00:00:01',
            issuer=name)
        self.assertEqual(expected, license.issuer)
        self.assertEqual(unknown, license.holder)

    def test_valid_holder(self):
        """Test LicenseData() for valid holder"""
        name = 'CN=name,O=organisation'
        expected = [('CN', 'name'), ('O', 'organisation')]
        unknown = Name(LicenseData.UNKNOWN_NAME)

        license = LicenseData(
            '2014-01-01T00:00:00',
            '2014-01-01T00:00:01',
            holder=name)
        self.assertEqual(unknown, license.issuer)
        self.assertEqual(expected, license.holder)

    def test_invalid_names(self):
        """Test LicenseData() for invalid names"""
        with self.assertRaises(ValueError):
            LicenseData(
                '2014-01-01T00:00:00',
                '2014-01-01T00:00:01',
                issuer='invalid')
        with self.assertRaises(ValueError):
            LicenseData(
                '2014-01-01T00:00:00',
                '2014-01-01T00:00:01',
                holder='invalid')

    def test_empty_subject(self):
        """Test LicenseData() for no subject"""
        license = LicenseData(
            '2014-01-01T00:00:00',
            '2014-01-01T00:00:01')
        self.assertEqual('', license.subject)

    def test_string_subject(self):
        """Test LicenseData() for string subject"""
        expected = 'subject'

        license = LicenseData(
            '2014-01-01T00:00:00',
            '2014-01-01T00:00:01',
            subject=expected)
        self.assertEqual(expected, license.subject)

    def test_int_subject(self):
        """Test LicenseData() for string subject"""
        expected = '42'

        license = LicenseData(
            '2014-01-01T00:00:00',
            '2014-01-01T00:00:01',
            subject=int(expected))
        self.assertEqual(expected, license.subject)

    def test_empty_consumer_type(self):
        """Test LicenseData() for no consumer_type"""
        license = LicenseData(
            '2014-01-01T00:00:00',
            '2014-01-01T00:00:01')
        self.assertEqual('', license.consumer_type)

    def test_string_consumer_type(self):
        """Test LicenseData() for string consumer_type"""
        expected = 'consumer type'

        license = LicenseData(
            '2014-01-01T00:00:00',
            '2014-01-01T00:00:01',
            consumer_type=expected)
        self.assertEqual(expected, license.consumer_type)

    def test_int_consumer_type(self):
        """Test LicenseData() for string consumer_type"""
        expected = '42'

        license = LicenseData(
            '2014-01-01T00:00:00',
            '2014-01-01T00:00:01',
            consumer_type=int(expected))
        self.assertEqual(expected, license.consumer_type)

    def test_string_info(self):
        """Test LicenseData() for string info"""
        expected = 'info'

        license = LicenseData(
            '2014-01-01T00:00:00',
            '2014-01-01T00:00:01',
            info=expected)
        self.assertEqual(expected, license.info)

    def test_empty_info(self):
        """Test LicenseData() for no info"""
        license = LicenseData(
            '2014-01-01T00:00:00',
            '2014-01-01T00:00:01')
        self.assertEqual('', license.info)

    def test_int_info(self):
        """Test LicenseData() for string info"""
        expected = '42'

        license = LicenseData(
            '2014-01-01T00:00:00',
            '2014-01-01T00:00:01',
            info=int(expected))
        self.assertEqual(expected, license.info)

    def test_string_extra(self):
        """Test LicenseData() for string extra data"""
        expected = 'hello world'

        license = LicenseData(
            '2014-01-01T00:00:00',
            '2014-01-01T00:00:01',
            extra=expected)
        self.assertEqual(expected, license.extra)

    def test_list_extra(self):
        """Test LicenseData() for list extra data"""
        extra = [1, 2, True, 'end']
        expected = '[1, 2, true, "end"]'

        license = LicenseData(
            '2014-01-01T00:00:00',
            '2014-01-01T00:00:01',
            extra=extra)
        self.assertEqual(expected, license.extra)

    def test_serialize(self):
        """Tests that a LicenseData can be serialised to XML"""
        expected = tostring(fromstring(
            '<object class="de.schlichtherle.license.LicenseContent">'
            '<void property="consumerType"><string /></void>'
            '<void property="extra">'
            '<string>{"hello": "world"}</string>'
            '</void>'
            '<void property="holder">'
            '<object class="javax.security.auth.x500.X500Principal">'
            '<string>CN=Unknown</string>'
            '</object>'
            '</void>'
            '<void property="info">'
            '<string>some information</string>'
            '</void>'
            '<void property="issued">'
            '<object class="java.util.Date">'
            '<long>1388534401000</long>'
            '</object>'
            '</void>'
            '<void property="issuer">'
            '<object class="javax.security.auth.x500.X500Principal">'
            '<string>CN=issuer</string>'
            '</object>'
            '</void>'
            '<void property="notAfter">'
            '<object class="java.util.Date">'
            '<long>1388534401000</long>'
            '</object>'
            '</void>'
            '<void property="notBefore">'
            '<object class="java.util.Date">'
            '<long>1388534400000</long>'
            '</object>'
            '</void>'
            '<void property="subject">'
            '<string>CN=subject</string>'
            '</void>'
            '</object>'))
        self.assertEqual(
            expected,
            tostring(serialize(LicenseData(
                '2014-01-01T00:00:00',
                '2014-01-01T00:00:01',
                '2014-01-01T00:00:01',
                issuer='CN=issuer',
                subject='CN=subject',
                info='some information',
                extra={'hello': 'world'}))))

    def test_deserialize(self):
        """Tests that a LicenseData can be serialised to XML"""
        license_data1 = LicenseData(
            '2014-01-01T00:00:00',
            '2014-01-01T00:00:01',
            '2014-01-01T00:00:01',
            issuer='CN=issuer',
            subject='subject',
            info='some information',
            extra={'hello': 'world'})
        license_data2 = deserialize(serialize(license_data1))
        self.assertEqual(
            license_data1.not_before,
            license_data2.not_before)
        self.assertEqual(
            license_data1.not_after,
            license_data2.not_after)
        self.assertEqual(
            license_data1.issued,
            license_data2.issued)
        self.assertEqual(
            license_data1.issuer,
            license_data2.issuer)
        self.assertEqual(
            license_data1.subject,
            license_data2.subject)
        self.assertEqual(
            license_data1.info,
            license_data2.info)
        self.assertEqual(
            license_data1.extra,
            license_data2.extra)
