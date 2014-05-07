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

from truepy import LicenseData


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
