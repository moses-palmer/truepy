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

class Name(list):
    """
    A class representing a simplified version of an X500 name.

    The string must be on the form "<type>=<value>[,<type>=<value,...].

    No escapes for <type> are supported, and only DQUOTE, PLUS, COMMA, SEMI,
    LANGLE and RANGLE are supported for <value>. Leading and trailing space is
    stripped for the value.
    """
    def __init__(self, name):
        # TODO: Implement
        pass
