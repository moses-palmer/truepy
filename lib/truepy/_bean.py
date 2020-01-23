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

from xml.etree import ElementTree

from . import tostring


def snake_to_camel(s):
    """Converts snake_case to camelCase.

    Consecutive underscores in the input will be treated as a single
    underscore. Trailing underscores will be discarded.

    :param str s: The snake case string to transform.

    :return: a camel case string
    :rtype: str
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
    """Converts camelCase to snake_case.

    :param str s: The camel case string to transform.

    :return: a snake case string
    :rtype: str
    """
    def characters():
        for c in s:
            if c.isupper():
                yield '_'
            yield c.lower()
    return ''.join(characters())


def value_to_xml(value, tag_name, class_name=None):
    """Serialises a value.

    The XML will be
        <object class="(class_name)">
            <(tag_name)>(value)</(tag_name)>
        </object>
    if class_name is given, otherwise
        <(tag_name)>(value)</(tag_name)>

    :param str value: The value.

    :param str tag_name: The tag name to use for the value.

    :param str class_name: The Java class name to use.

    :return: an element
    :rtype: xml.etree.ElementTree.Element
    """
    if class_name is None:
        o = ElementTree.Element(tag_name)
        o.text = value
    else:
        o = ElementTree.Element('object', attrib={
            'class': class_name})
        o.append(value_to_xml(value, tag_name))

    return o


#: A mapping of serialiser name to serialiser
_SERIALIZERS = {}


def bean_serializer(*value_types):
    """Marks a function as a serialiser for a specific type.

    The function must return an xml.etree.ElementTree.Element. It is passed a
    single value.

    :param value_types: The types that this serialiser is capable of
        serialising.
    """
    def inner(f):
        for value_type in value_types:
            _SERIALIZERS[value_type] = f
        return f

    return inner


def _serialize_object(value):
    """Serialises an object.

    The object must have the attribute 'bean_class'.

    All properties of the object are wrapped in
    <void property="(name)"></void>, and must thus themselves be serialisable.

    :param object value: The value to serialise.

    :return: an element
    :rtype: xml.etree.ElementTree.Element
    """
    try:
        class_name = getattr(value, 'bean_class')
    except AttributeError:
        raise ValueError('unknown Java class')

    property_names = sorted(
        k
        for k, v in o.__class__.__dict__.items()
        if isinstance(getattr(o.__class__, k), property))

    java_wrapper = ElementTree.Element('java', attrib={
        'version': '1.0',
        'class': 'java.beans.XMLDecoder'})

    container = ElementTree.SubElement(java_wrapper, 'object', attrib={
        'class': class_name})
    for property_name in property_names:
        container.append(
            serialize(property_name, getattr(o, property_name)))

    return java_wrapper


def serialize(value):
    """Serialises a value.

    The value type must have a serialiser registered, or be an object with the
    attribute 'bean_class' whose properties can be serialised with serialize.

    :param object value: The value to serialise.

    :return: an element describing the value
    :rtype: xml.etree.ElementTree.Element

    :raises ValueError: if the value cannot be serialised
    """
    try:
        return _SERIALIZERS[type(value)](value)
    except KeyError:
        pass

    try:
        class_name = getattr(value, 'bean_class')
    except AttributeError:
        raise ValueError('unknown Java class for %s', type(value))

    property_names = sorted(
        k
        for k, v in value.__class__.__dict__.items()
        if isinstance(getattr(value.__class__, k), property))

    xml = ElementTree.Element('object', attrib={
        'class': class_name})
    for property_name in property_names:
        property_value = serialize(getattr(value, property_name))
        property_container = ElementTree.SubElement(xml, 'void', attrib={
            'property': snake_to_camel(property_name)})
        property_container.append(property_value)

    return xml


def to_document(e):
    """Transforms a serialised value to an XML document.

    The serialised value will be wrapped in a `<java>` tag and an XML
    declaration will be prepended.

    :param str s: The serialised value.

    :return: a valid XML document string
    :rtype: str
    """
    return (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<java version="1.0" class="java.beans.XMLDecoder">'
        '%s'
        '</java>') % tostring(e)


class UnknownFragmentException(Exception):
    """The exception raised by a deserialiser when it cannot handle an XML
    fragment.
    """
    pass


#: A mapping from deserialiser name to deserialiser
_DESERIALIZERS = []


def bean_deserializer(f):
    """Marks a function as a deserialiser.

    The function is passed an xml.etree.ElementTree.Element. If the function is
    not capable of deserialising the XML, it must raise
    UnknownFragmentException.
    """
    _DESERIALIZERS.append(f)
    return f


def deserialize(element):
    """Deserialises a value.

    The value type must have a serialiser registered, or be an object with the
    attribute 'bean_class' whose properties can be serialised with serialize.

    :param xml.etree.ElementTree.Element element: The XML fragment to
        serialise.

    :return: a value
    :rtype: object

    :raises ValueError: if the value cannot be serialised
    """
    for deserializer in _DESERIALIZERS:
        try:
            return deserializer(element)
        except UnknownFragmentException:
            pass

    raise ValueError('unknown XML fragment: %s', ElementTree.tostring(element))


from  ._bean_serializers import *
