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


def snake_to_camel(s):
    """
    Converts snake_case to camelCase.

    Consecutive underscores in the input will be treated as a single underscore.
    Trailing underscores will be discarded.

    @param s
        The snake case string to transform.
    @return a camel case string
    """
    def characters():
        was_underscore = False
        for c in s:
            if c == '_':
                was_underscore = True
            else:
                yield c.upper() if was_underscore else c
                was_underscore = False
    return ''.join(characters())


def camel_to_snake(s):
    """
    Converts camelCase to snake_case.

    @param s
        The camel case string to transform.
    @return a snake case string
    """
    def characters():
        for c in s:
            if c.isupper():
                yield '_'
            yield c.lower()
    return ''.join(characters())
