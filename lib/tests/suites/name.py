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

from truepy import Name, tostring
from truepy._bean import serialize


@test
def Name_escape0():
    """Tests that Name.escape for string not needing escaping returns the input
    string"""
    s = 'hello world'
    expected = s

    assert_eq(expected, Name.escape(s))


@test
def Name_escape1():
    """Tests that Name.escape for string needing escaping returns the correct
    string"""
    s = 'hello, "world"; insert <token + value>'
    expected = 'hello#2C #22world#22#3B insert #3Ctoken #2B value#3E'

    assert_eq(expected, Name.escape(s))


@test
def Name_unescape0():
    """Tests that Name.unescape for unescaped string returns the input string"""
    s = 'hello world'
    expected = s

    assert_eq(expected, Name.unescape(s))


@test
def Name_unescape1():
    """Tests that Name.unescape for escaped string returns the correct string"""
    s = 'hello, "world"; insert <token + value>'

    assert_eq(s, Name.unescape(Name.escape(s)))


@test
def Name_unescape2():
    """Tests that Name.unescape for escaped string with invalid escape seqienmce
    raises ValueError"""
    with assert_exception(ValueError):
        Name.unescape('#01')


@test
def Name_valid_string():
    """Tests Name() from valid string returns the correct sequence"""
    assert_eq(
        [('CN', '<token>'), ('O', 'organisation')],
        Name('CN=#3Ctoken#3E,O=organisation'))


@test
def Name_invalid_string():
    """Tests that Name() from invalid string raises ValueError"""
    with assert_exception(ValueError):
        Name('CN=invalid escape sequence#01')
    with assert_exception(ValueError):
        Name('CN=valid escape sequence, no type')


@test
def Name_str0():
    """Tests that str(Name()) return the input string"""
    s = 'CN=#3Ctoken#3E,O=organisation'
    assert_eq(s, str(Name(s)))


@test
def Name_str1():
    """Tests that str(Name()) return the input string with leading and trailing
    space stripped for values"""
    s = 'CN=#3Ctoken#3E , O=organisation '
    expected = 'CN=#3Ctoken#3E,O=organisation'
    assert_eq(expected, str(Name(s)))


@test
def Name_serialize0():
    """Tests that a name can be serialised to XML"""
    s = 'CN=#3Ctoken#3E , O=organisation '

    assert_eq(
        '<object class="javax.security.auth.x500.X500Principal">'
            '<string>CN=#3Ctoken#3E,O=organisation</string>'
        '</object>',
        tostring(serialize(Name(s))))
