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

from truepy import LicenseData, Name, fromstring, tostring
from truepy._bean import deserialize, serialize


@test
def LicenseData_valid_validity_window():
    """Test LicenseData() for valid validity window"""
    LicenseData('2014-01-01T00:00:00', '2014-01-01T00:00:01')


@test
def LicenseData_invalid_validity_window():
    """Test LicenseData() for invalid validity window"""
    with assert_exception(ValueError):
        LicenseData('2014-01-01T00:00:00', '2014-01-01T00:00:00')
    with assert_exception(ValueError):
        LicenseData('2014-01-01T00:00:01', '2014-01-01T00:00:00')


@test
def LicenseData_issued():
    """Test LicenseData.issued for unspecified issued value"""
    license = LicenseData(
        '2014-01-01T00:00:00',
        '2014-01-01T00:00:01')
    assert_eq(license.issued, license.not_before)


@test
def LicenseData_issued():
    """Test LicenseData.issued for specified issued value"""
    license = LicenseData(
        '2014-01-01T00:00:00',
        '2014-01-01T00:00:01',
        '2014-01-01T00:00:01')
    assert_eq(license.issued, license.not_after)


@test
def LicenseData_invalid_timestamps():
    """Test LicenseData() for invalid timestamps"""
    with assert_exception(ValueError):
        LicenseData(
            'invalid',
            '2014-01-01T00:00:01',
            '2014-01-01T00:00:03')
    with assert_exception(ValueError):
        LicenseData(
            '2014-01-01T00:00:00',
            'invalid',
            '2014-01-01T00:00:03')
    with assert_exception(ValueError):
        LicenseData(
            '2014-01-01T00:00:00',
            '2014-01-01T00:00:01',
            'invalid')


@test
def LicenseData_valid_issuer():
    """Test LicenseData() for valid issuer"""
    name = 'CN=name,O=organisation'
    expected = [('CN', 'name'), ('O', 'organisation')]
    unknown = Name(LicenseData.UNKNOWN_NAME)

    license = LicenseData(
        '2014-01-01T00:00:00',
        '2014-01-01T00:00:01',
        issuer = name)
    assert_eq(expected, license.issuer)
    assert_eq(unknown, license.holder)


@test
def LicenseData_valid_holder():
    """Test LicenseData() for valid holder"""
    name = 'CN=name,O=organisation'
    expected = [('CN', 'name'), ('O', 'organisation')]
    unknown = Name(LicenseData.UNKNOWN_NAME)

    license = LicenseData(
        '2014-01-01T00:00:00',
        '2014-01-01T00:00:01',
        holder = name)
    assert_eq(unknown, license.issuer)
    assert_eq(expected, license.holder)


@test
def LicenseData_invalid_names():
    """Test LicenseData() for invalid names"""
    with assert_exception(ValueError):
        license = LicenseData(
            '2014-01-01T00:00:00',
            '2014-01-01T00:00:01',
            issuer = 'invalid')
    with assert_exception(ValueError):
        license = LicenseData(
            '2014-01-01T00:00:00',
            '2014-01-01T00:00:01',
            holder = 'invalid')


@test
def LicenseData_empty_subject():
    """Test LicenseData() for no subject"""
    license = LicenseData(
        '2014-01-01T00:00:00',
        '2014-01-01T00:00:01')
    assert_eq('', license.subject)


@test
def LicenseData_string_subject():
    """Test LicenseData() for string subject"""
    expected = 'subject'

    license = LicenseData(
        '2014-01-01T00:00:00',
        '2014-01-01T00:00:01',
        subject = expected)
    assert_eq(expected, license.subject)


@test
def LicenseData_int_subject():
    """Test LicenseData() for string subject"""
    expected = '42'

    license = LicenseData(
        '2014-01-01T00:00:00',
        '2014-01-01T00:00:01',
        subject = int(expected))
    assert_eq(expected, license.subject)


@test
def LicenseData_empty_consumer_type():
    """Test LicenseData() for no consumer_type"""
    license = LicenseData(
        '2014-01-01T00:00:00',
        '2014-01-01T00:00:01')
    assert_eq('', license.consumer_type)


@test
def LicenseData_string_consumer_type():
    """Test LicenseData() for string consumer_type"""
    expected = 'consumer type'

    license = LicenseData(
        '2014-01-01T00:00:00',
        '2014-01-01T00:00:01',
        consumer_type = expected)
    assert_eq(expected, license.consumer_type)


@test
def LicenseData_int_consumer_type():
    """Test LicenseData() for string consumer_type"""
    expected = '42'

    license = LicenseData(
        '2014-01-01T00:00:00',
        '2014-01-01T00:00:01',
        consumer_type = int(expected))
    assert_eq(expected, license.consumer_type)


@test
def LicenseData_string_information():
    """Test LicenseData() for string information"""
    expected = 'information'

    license = LicenseData(
        '2014-01-01T00:00:00',
        '2014-01-01T00:00:01',
        information = expected)
    assert_eq(expected, license.information)


@test
def LicenseData_empty_information():
    """Test LicenseData() for no information"""
    license = LicenseData(
        '2014-01-01T00:00:00',
        '2014-01-01T00:00:01')
    assert_eq('', license.information)


@test
def LicenseData_string_information():
    """Test LicenseData() for string information"""
    expected = 'information'

    license = LicenseData(
        '2014-01-01T00:00:00',
        '2014-01-01T00:00:01',
        information = expected)
    assert_eq(expected, license.information)


@test
def LicenseData_int_information():
    """Test LicenseData() for string information"""
    expected = '42'

    license = LicenseData(
        '2014-01-01T00:00:00',
        '2014-01-01T00:00:01',
        information = int(expected))
    assert_eq(expected, license.information)


@test
def LicenseData_string_extra():
    """Test LicenseData() for string extra data"""
    expected = 'hello world'

    license = LicenseData(
        '2014-01-01T00:00:00',
        '2014-01-01T00:00:01',
        extra = expected)
    assert_eq(expected, license.extra)


@test
def LicenseData_list_extra():
    """Test LicenseData() for list extra data"""
    extra = [1, 2, True, 'end']
    expected = '[1, 2, true, "end"]'

    license = LicenseData(
        '2014-01-01T00:00:00',
        '2014-01-01T00:00:01',
        extra = extra)
    assert_eq(expected, license.extra)


@test
def LicenseData_serialize():
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
            '<void property="information">'
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
    assert_eq(expected,
        tostring(serialize(LicenseData(
            '2014-01-01T00:00:00',
            '2014-01-01T00:00:01',
            '2014-01-01T00:00:01',
            issuer = 'CN=issuer',
            subject = 'CN=subject',
            information = 'some information',
            extra = {'hello': 'world'}))))


@test
def LicenseData_deserialize():
    """Tests that a LicenseData can be serialised to XML"""
    license_data1 = LicenseData(
        '2014-01-01T00:00:00',
        '2014-01-01T00:00:01',
        '2014-01-01T00:00:01',
        issuer = 'CN=issuer',
        subject = 'subject',
        information = 'some information',
        extra = {'hello': 'world'})
    license_data2 = deserialize(serialize(license_data1))
    assert_eq(
        license_data1.not_before,
        license_data2.not_before)
    assert_eq(
        license_data1.not_after,
        license_data2.not_after)
    assert_eq(
        license_data1.issued,
        license_data2.issued)
    assert_eq(
        license_data1.issuer,
        license_data2.issuer)
    assert_eq(
        license_data1.subject,
        license_data2.subject)
    assert_eq(
        license_data1.information,
        license_data2.information)
    assert_eq(
        license_data1.extra,
        license_data2.extra)
