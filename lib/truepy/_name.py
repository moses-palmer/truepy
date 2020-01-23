# coding: utf-8
# truepy
# Copyright (C) 2014-2020 Moses Palmér
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

import cryptography.x509
import re

from ._bean import bean_serializer, value_to_xml
from ._bean_serializers import bean_class


@bean_class('javax.security.auth.x500.X500Principal')
class Name(list):
    #: The escapable characters
    ESCAPABLES = ('"', '+', ',', ';', '<', '>')

    #: A mapping from short attribute names to OIDs
    ATTRIBUTES = {
        'C': cryptography.x509.OID_COUNTRY_NAME,
        'O': cryptography.x509.OID_ORGANIZATION_NAME,
        'OU': cryptography.x509.OID_ORGANIZATIONAL_UNIT_NAME,
        'ST': cryptography.x509.OID_STATE_OR_PROVINCE_NAME,
        'CN': cryptography.x509.OID_COMMON_NAME,
        'L': cryptography.x509.OID_LOCALITY_NAME,
        'SN': cryptography.x509.OID_SURNAME,
        'GN': cryptography.x509.OID_GIVEN_NAME}

    #: The reversed mapping from `attr`:ATTRIBUTES
    REVERSED_ATTRIBUTES = {
        value: key
        for key, value in ATTRIBUTES.items()}

    SUB_RE = re.compile(r'\#([0-9a-fA-F]{2})')

    @classmethod
    def _bean_deserialize(self, element):
        return self(element.find('.//string').text)

    @classmethod
    def escape(self, s):
        """Escapes a string.

        :param str s: The string to escape.

        :return: an escaped string
        :rtype: str
        """
        return ''.join(
            '#%02X' % ord(c) if c in self.ESCAPABLES else c
            for c in s)

    @classmethod
    def unescape(self, s):
        """Unescapes a string.

        This is the inverse operation to escape.

        :param str s: The string to unescape.
        :return: an unescaped string
        :rtype: str

        :raises ValueError: if an invalid escape is encountered; only
            characters in :attr:`ESCAPABLES` are supported
        """
        def replacer(m):
            char = chr(int(m.group(1), 16))
            if char not in self.ESCAPABLES:
                raise ValueError('invalid escape sequence: %s', m.group(0))
            return char

        return self.SUB_RE.sub(replacer, s)

    def __init__(self, name):
        """A class representing a simplified version of an X500 name.

        The string must be on the form
        ``'<type>=<value>[,<type>=<value,...]'``.

        No escapes for ``<type>`` are supported, and only ``DQUOTE``, ``PLUS``,
        ``COMMA``, ``SEMI``, ``LANGLE`` and ``RANGLE`` are supported for
        ``<value>``.

        Leading and trailing space is stripped for the value.

        :param name: The *X.509* name string from which to create this
            instance. This may also be a list of the tuple ``(type, value)``.
        :type name: str or list

        :raises ValueError: if any part contains an invalid escape sequence, or
            any part does not contain an ``'='``
        """
        if isinstance(name, list):
            self.extend(name)
        else:
            try:
                self.extend(
                    (
                        kv.split('=')[0].strip(),
                        self.unescape(kv.split('=')[1].strip()))
                    for kv in name.split(','))
            except IndexError:
                raise ValueError('invalid X509 name: %s', name)

    def __str__(self):
        return ','.join(
            '%s=%s' % (k, self.escape(v))
            for (k, v) in self)

    @classmethod
    def from_x509_name(self, name):
        """Creates a name from a :class:`cryptography.x509.Name`.

        :param cryptography.x509.Name name: The source name.
        """
        return self([
            (self.REVERSED_ATTRIBUTES[na.oid], na.value)
            for na in name])


@bean_serializer(Name)
def name_serializer(v):
    """Serialises a truepy.Name instance to a
    javax.security.auth.x500.X500Principal"""
    return value_to_xml(
        str(v), 'string', Name.bean_class)
