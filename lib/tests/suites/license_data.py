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

from truepy import LicenseData, Name


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
