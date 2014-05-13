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

from truepy import LicenseData, License
from truepy._bean import serialize, to_document


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
