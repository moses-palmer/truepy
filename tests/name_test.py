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

from truepy import Name, tostring
from truepy._bean import serialize


class NameTest(unittest.TestCase):
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
