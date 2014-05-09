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


from truepy import fromstring, tostring
from truepy._bean import snake_to_camel, camel_to_snake
from truepy._bean import value_to_xml
from truepy._bean import serialize


@test
def snake_to_camel0():
    """Tests that snake_to_camel works as expected"""
    assert_eq('camelCase', snake_to_camel('camel_case'))
    assert_eq('camelCase', snake_to_camel('camel__case'))
    assert_eq('camelCase', snake_to_camel('camel_case_'))
    assert_eq('CamelCase', snake_to_camel('_camel_case'))


@test
def camel_to_snake0():
    """Tests that camel_to_snake works as expected"""
    assert_eq('snake_case', camel_to_snake('snakeCase'))
    assert_eq('_snake_case', camel_to_snake('SnakeCase'))
    assert_eq('_s_n_a_k_e', camel_to_snake('SNAKE'))


@test
def value_to_xml0():
    """Tests value_to_xml for no class name"""
    assert_eq(
        '<test>value</test>',
        tostring(value_to_xml('value', 'test')))


@test
def value_to_xml1():
    """Tests value_to_xml for a class name"""
    assert_eq(
        '<object class="test">'
            '<tag>value</tag>'
        '</object>',
        tostring(value_to_xml('value', 'tag', 'test')))


@test
def serialize0():
    """Serialises an unknown value"""
    class unknown(object):
        pass

    with assert_exception(ValueError):
        serialize(unknown())


@test
def serialize1():
    """Serialises an empty class"""
    class empty(object):
        bean_class = 'test.class'

    assert_eq(
        '<object class="test.class" />',
        tostring(serialize(empty())))


@test
def serialize2():
    """Serialises a class with an unknown property"""
    class unknown(object):
        pass

    class has_unknown(object):
        bean_class = 'test.class'
        @property
        def a(self):
            return unknown()

    with assert_exception(ValueError):
        serialize(has_unknown())


@test
def serialize3():
    """Serialises a string"""
    assert_eq(
        '<string>hello world</string>',
        tostring(serialize('hello world')))


@test
def serialize4():
    """Serialises an object"""
    class test(object):
        bean_class = 'test.class'
        @property
        def z(self):
            return True
        @property
        def last(self):
            return 42
        @property
        def first(self):
            return 'hello world'

    assert_eq(
        '<object class="test.class">'
            '<void property="first">'
                '<string>hello world</string>'
            '</void>'
            '<void property="last">'
                '<int>42</int>'
            '</void>'
            '<void property="z">'
                '<boolean>true</boolean>'
            '</void>'
        '</object>',
        tostring(serialize(test())))
