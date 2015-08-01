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


from datetime import datetime

from truepy import fromstring, tostring
from truepy._bean import snake_to_camel, camel_to_snake
from truepy._bean import value_to_xml
from truepy._bean import deserialize, serialize, to_document
from truepy._bean_serializers import _DESERIALIZER_CLASSES, bean_class


class BeanTest(unittest.TestCase):
    def test_snake_to_camel(self):
        """Tests that snake_to_camel works as expected"""
        self.assertEqual(
            'camelCase',
            snake_to_camel('camel_case'))
        self.assertEqual(
            'camelCase',
            snake_to_camel('camel__case'))
        self.assertEqual(
            'camelCase',
            snake_to_camel('camel_case_'))
        self.assertEqual(
            'CamelCase',
            snake_to_camel('_camel_case'))

    def test_camel_to_snake(self):
        """Tests that camel_to_snake works as expected"""
        self.assertEqual('snake_case', camel_to_snake('snakeCase'))
        self.assertEqual('_snake_case', camel_to_snake('SnakeCase'))
        self.assertEqual('_s_n_a_k_e', camel_to_snake('SNAKE'))

    def test_value_to_xml_no_class(self):
        """Tests value_to_xml for no class name"""
        self.assertEqual(
            '<test>value</test>',
            tostring(value_to_xml('value', 'test')))

    def test_value_to_xml_with_class(self):
        """Tests value_to_xml for a class name"""
        self.assertEqual(
            '<object class="test">'
            '<tag>value</tag>'
            '</object>',
            tostring(value_to_xml('value', 'tag', 'test')))

    def test_serialize_unknown(self):
        """Serialises an unknown value"""
        class unknown(object):
            pass

        with self.assertRaises(ValueError):
            serialize(unknown())

    def test_serialize_empty_class(self):
        """Serialises an empty class"""
        class empty(object):
            bean_class = 'test.class'

        self.assertEqual(
            '<object class="test.class" />',
            tostring(serialize(empty())))

    def test_serialize_unknown_property(self):
        """Serialises a class with an unknown property"""
        class unknown(object):
            pass

        class has_unknown(object):
            bean_class = 'test.class'

            @property
            def test_a(self):
                return unknown()

        with self.assertRaises(ValueError):
            serialize(has_unknown())

    def test_serialize_string(self):
        """Serialises a string"""
        self.assertEqual(
            '<string>hello world</string>',
            tostring(serialize('hello world')))

    def test_serialize_object(self):
        """Serialises an object"""
        class test(object):
            bean_class = 'test.class'

            @property
            def test_property(self):
                return True

        self.assertEqual(
            '<object class="test.class">'
            '<void property="testProperty">'
            '<boolean>true</boolean>'
            '</void>'
            '</object>',
            tostring(serialize(test())))

    def test_serialize_datetime(self):
        """Serialises datetime instances"""
        self.assertEqual(
            '<object class="java.util.Date">'
            '<long>0</long>'
            '</object>',
            tostring(serialize(
                datetime.strptime('1970-01-01 UTC', '%Y-%m-%d %Z'))))

        self.assertEqual(
            '<object class="java.util.Date">'
            '<long>86400000</long>'
            '</object>',
            tostring(serialize(
                datetime.strptime('1970-01-02 UTC', '%Y-%m-%d %Z'))))

    def test_deserialize_unknown_fragment(self):
        """Deserialises an unknown fragment"""
        with self.assertRaises(ValueError):
            deserialize(fromstring(
                '<object class="unknown">'
                '<void property="a">'
                '<int>42</int>'
                '</void>'
                '</object>'))

    def test_deserialize(self):
        """Deserialises invalid fragments"""
        with self.assertRaises(ValueError):
            deserialize(fromstring(
                '<boolean>invalid</boolean>'))
        with self.assertRaises(ValueError):
            deserialize(fromstring(
                '<int>invalid</int>'))

    def test_deserialize_known_fragment(self):
        """Deserialises known fragments"""
        self.assertEqual(
            True,
            deserialize(fromstring(
                '<boolean>true</boolean>')))
        self.assertEqual(
            42,
            deserialize(fromstring(
                '<int>42</int>')))
        self.assertEqual(
            'hello world',
            deserialize(fromstring(
                '<string>hello world</string>')))

    def test_deserialize_with_constructor(self):
        """Deserialises an object using constructor"""
        global _DESERIALIZER_CLASSES
        class_name = 'test.class'

        try:
            @bean_class(class_name)
            class test(object):
                @property
                def test_a(selfself):
                    return self._a

                def test___init__(self, a):
                    self._a = a

            o = deserialize(fromstring(
                '<object class="test.class">'
                '<void property="a">'
                '<string>hello world</string>'
                '</void>'
                '</object>'))
            self.assertEqual('hello world', o.a)
            self.assertEqual(test, o.__class__)

        finally:
            del _DESERIALIZER_CLASSES[class_name]

    def test_deserialize_datetime(self):
        """Deserialises datetime objects"""
        expected = datetime.strptime('2014-01-01 UTC', '%Y-%m-%d %Z')
        self.assertEqual(
            expected,
            deserialize(serialize(expected)))

    def test_to_document(self):
        """Tests that todocument creates a valid XML document"""
        expected = 'hello world'

        self.assertEqual(
            expected,
            deserialize(
                fromstring(
                    to_document(
                        serialize(expected)))
                [0]))
