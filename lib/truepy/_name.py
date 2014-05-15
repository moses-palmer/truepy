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

import re

from ._bean import bean_serializer, value_to_xml
from ._bean_serializers import bean_class


@bean_class('javax.security.auth.x500.X500Principal')
class Name(list):
    """
    A class representing a simplified version of an X500 name.

    The string must be on the form "<type>=<value>[,<type>=<value,...].

    No escapes for <type> are supported, and only DQUOTE, PLUS, COMMA, SEMI,
    LANGLE and RANGLE are supported for <value>. Leading and trailing space is
    stripped for the value.
    """
    ESCAPABLES = ('"', '+', ',', ';', '<', '>')

    SUB_RE = re.compile(r'\#([0-9a-fA-F]{2})')

    @classmethod
    def bean_deserialize(self, element):
        return self(element.find('.//string').text)

    @classmethod
    def escape(self, s):
        """
        Escapes a string.

        @param s
            The string to escape.
        @return an escaped string
        """
        return ''.join('#%02X' % ord(c) if c in self.ESCAPABLES else c
            for c in s)

    @classmethod
    def unescape(self, s):
        """
        Unescapes a string.

        This is the inverse operation to escape.

        @param s
            The string to unescape.
        @return an unescaped string
        @raise ValueError if an invalid escape is encountered; only characters
            in ESCAPABLES are supported
        """
        def replacer(m):
            char = chr(int(m.group(1), 16))
            if not char in self.ESCAPABLES:
                raise ValueError('invalid escape sequence: %s', m.group(0))
            return char

        return self.SUB_RE.sub(replacer, s)

    def __init__(self, name):
        """
        Creates a new instance of Name from a string.

        @param name
            The X509 name string from which to create this Name.
        @raise ValueError if any part contains an invalid escape sequence, or
            any part does not contain an '='
        """
        try:
            self.extend(
                (
                    kv.split('=')[0].strip(),
                    self.unescape(kv.split('=')[1].strip()))
                for kv in name.split(','))
        except IndexError:
            raise ValueError('invalid X509 name: %s', name)

    def __str__(self):
        return ','.join('%s=%s' % (k, self.escape(v))
            for (k, v) in self)


@bean_serializer(Name)
def name_serializer(v):
    """Serialises a truepy.Name instance to a
    javax.security.auth.x500.X500Principal"""
    return value_to_xml(
        str(v), 'string', Name.bean_class)
