# generated from rosidl_generator_py/resource/_idl.py.em
# with input from ferrobotics:msg/ACFTelem.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_ACFTelem(type):
    """Metaclass of message 'ACFTelem'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('ferrobotics')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'ferrobotics.msg.ACFTelem')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__acf_telem
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__acf_telem
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__acf_telem
            cls._TYPE_SUPPORT = module.type_support_msg__msg__acf_telem
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__acf_telem

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ACFTelem(metaclass=Metaclass_ACFTelem):
    """Message class 'ACFTelem'."""

    __slots__ = [
        '_id',
        '_force',
        '_position',
        '_in_contact',
        '_in_error',
        '_errors',
        '_error_messages',
    ]

    _fields_and_field_types = {
        'id': 'int32',
        'force': 'float',
        'position': 'float',
        'in_contact': 'boolean',
        'in_error': 'boolean',
        'errors': 'boolean[8]',
        'error_messages': 'sequence<string>',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.Array(rosidl_parser.definition.BasicType('boolean'), 8),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.UnboundedString()),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.id = kwargs.get('id', int())
        self.force = kwargs.get('force', float())
        self.position = kwargs.get('position', float())
        self.in_contact = kwargs.get('in_contact', bool())
        self.in_error = kwargs.get('in_error', bool())
        self.errors = kwargs.get(
            'errors',
            [bool() for x in range(8)]
        )
        self.error_messages = kwargs.get('error_messages', [])

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.id != other.id:
            return False
        if self.force != other.force:
            return False
        if self.position != other.position:
            return False
        if self.in_contact != other.in_contact:
            return False
        if self.in_error != other.in_error:
            return False
        if self.errors != other.errors:
            return False
        if self.error_messages != other.error_messages:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property  # noqa: A003
    def id(self):  # noqa: A003
        """Message field 'id'."""
        return self._id

    @id.setter  # noqa: A003
    def id(self, value):  # noqa: A003
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'id' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'id' field must be an integer in [-2147483648, 2147483647]"
        self._id = value

    @builtins.property
    def force(self):
        """Message field 'force'."""
        return self._force

    @force.setter
    def force(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'force' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'force' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._force = value

    @builtins.property
    def position(self):
        """Message field 'position'."""
        return self._position

    @position.setter
    def position(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'position' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'position' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._position = value

    @builtins.property
    def in_contact(self):
        """Message field 'in_contact'."""
        return self._in_contact

    @in_contact.setter
    def in_contact(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'in_contact' field must be of type 'bool'"
        self._in_contact = value

    @builtins.property
    def in_error(self):
        """Message field 'in_error'."""
        return self._in_error

    @in_error.setter
    def in_error(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'in_error' field must be of type 'bool'"
        self._in_error = value

    @builtins.property
    def errors(self):
        """Message field 'errors'."""
        return self._errors

    @errors.setter
    def errors(self, value):
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 len(value) == 8 and
                 all(isinstance(v, bool) for v in value) and
                 True), \
                "The 'errors' field must be a set or sequence with length 8 and each value of type 'bool'"
        self._errors = value

    @builtins.property
    def error_messages(self):
        """Message field 'error_messages'."""
        return self._error_messages

    @error_messages.setter
    def error_messages(self, value):
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, str) for v in value) and
                 True), \
                "The 'error_messages' field must be a set or sequence and each value of type 'str'"
        self._error_messages = value
