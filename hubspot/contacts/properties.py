##############################################################################
#
# Copyright (c) 2014, 2degrees Limited.
# All Rights Reserved.
#
# This file is part of hubspot-contacts
# <https://github.com/2degrees/hubspot-contacts>, which is subject to the
# provisions of the BSD at
# <http://dev.2degreesnetwork.com/p/2degrees-license.html>. A copy of the
# license should accompany this distribution. THIS SOFTWARE IS PROVIDED "AS IS"
# AND ANY AND ALL EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT
# NOT LIMITED TO, THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST
# INFRINGEMENT, AND FITNESS FOR A PARTICULAR PURPOSE.
#
##############################################################################

from pyrecord import Record
from voluptuous import Any
from voluptuous import Schema


Property = Record.create_type(
    'Property',
    'name',
    'label',
    'description',
    'group_name',
    'field_widget',
    )
BooleanProperty = Property.extend_type('BooleanProperty')
DatetimeProperty = Property.extend_type('DatetimeProperty')
EnumerationProperty = Property.extend_type('EnumerationProperty', 'options')
NumberProperty = Property.extend_type('NumberProperty')
StringProperty = Property.extend_type('StringProperty')


PROPERTY_TYPE_BY_NAME = {
    'bool': BooleanProperty,
    'datetime': DatetimeProperty,
    'enumeration': EnumerationProperty,
    'number': NumberProperty,
    'string': StringProperty,
    }


_GET_ALL_PROPERTIES_RESPONSE_SCHEMA_DEFINITION = [
    {
        'name': unicode,
        'type': Any(*PROPERTY_TYPE_BY_NAME.keys()),
        'options': [],
        }
    ]


_GET_ALL_PROPERTIES_RESPONSE_SCHEMA = Schema(
    _GET_ALL_PROPERTIES_RESPONSE_SCHEMA_DEFINITION,
    required=True,
    extra=True,
    )


def get_all_properties(connection):
    properties_data = connection.send_get_request('/properties')
    _GET_ALL_PROPERTIES_RESPONSE_SCHEMA(properties_data)

    properties = []
    for property_data in properties_data:
        property_ = _build_property_specialization_from_data(property_data)
        properties.append(property_)
    return properties


def _build_property_specialization_from_data(property_data):
    property_generalization = \
        _build_property_generalization_from_data(property_data)

    property_type_name = property_data['type']
    property_type = PROPERTY_TYPE_BY_NAME[property_type_name]

    if issubclass(property_type, EnumerationProperty):
        enumeration_options_data = property_data['options']
        enumeration_options = \
            _build_enumeration_options_from_data(enumeration_options_data)
        additional_field_values = {'options': enumeration_options}
    else:
        additional_field_values = {}

    property_specialization = property_type.init_from_generalization(
        property_generalization,
        **additional_field_values
        )

    return property_specialization


def _build_property_generalization_from_data(property_data):
    property_ = Property(
        property_data['name'],
        property_data['label'],
        property_data['description'],
        property_data['groupName'],
        property_data['fieldType'],
        )
    return property_


def _build_enumeration_options_from_data(enumeration_options_data):
    enumeration_options = {}
    for option_data in enumeration_options_data:
        option_label = option_data['label']
        option_value = option_data['value']
        enumeration_options[option_label] = option_value
    return enumeration_options
