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

from ._bean import bean_serializer, bean_deserializer, value_to_xml, \
    UnknownFragmentException


@bean_serializer(bool)
def str_serializer(value):
    return value_to_xml('true' if value else 'false', 'boolean')


@bean_serializer(int)
def str_serializer(value):
    return value_to_xml(str(value), 'int')


@bean_serializer(str)
def str_serializer(value):
    return value_to_xml(value, 'string')


@bean_deserializer
def bool_deserializer(element):
    if element.tag == 'boolean':
        value = element.text.strip()
        if value == 'true':
            return True
        elif value == 'false':
            return False
        else:
            raise ValueError('invalid boolean value: %s', value)
    else:
        raise UnknownFragmentException()


@bean_deserializer
def int_deserializer(element):
    if element.tag == 'int':
        return int(element.text.strip())
    else:
        raise UnknownFragmentException()


@bean_deserializer
def str_deserializer(element):
    if element.tag == 'string':
        return (element.text or '').strip()
    else:
        raise UnknownFragmentException()
