// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from ferrobotics:msg/ACFTelem.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "ferrobotics/msg/detail/acf_telem__rosidl_typesupport_introspection_c.h"
#include "ferrobotics/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "ferrobotics/msg/detail/acf_telem__functions.h"
#include "ferrobotics/msg/detail/acf_telem__struct.h"


// Include directives for member types
// Member `error_messages`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__ACFTelem_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  ferrobotics__msg__ACFTelem__init(message_memory);
}

void ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__ACFTelem_fini_function(void * message_memory)
{
  ferrobotics__msg__ACFTelem__fini(message_memory);
}

size_t ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__size_function__ACFTelem__errors(
  const void * untyped_member)
{
  (void)untyped_member;
  return 8;
}

const void * ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__get_const_function__ACFTelem__errors(
  const void * untyped_member, size_t index)
{
  const bool * member =
    (const bool *)(untyped_member);
  return &member[index];
}

void * ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__get_function__ACFTelem__errors(
  void * untyped_member, size_t index)
{
  bool * member =
    (bool *)(untyped_member);
  return &member[index];
}

void ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__fetch_function__ACFTelem__errors(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const bool * item =
    ((const bool *)
    ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__get_const_function__ACFTelem__errors(untyped_member, index));
  bool * value =
    (bool *)(untyped_value);
  *value = *item;
}

void ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__assign_function__ACFTelem__errors(
  void * untyped_member, size_t index, const void * untyped_value)
{
  bool * item =
    ((bool *)
    ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__get_function__ACFTelem__errors(untyped_member, index));
  const bool * value =
    (const bool *)(untyped_value);
  *item = *value;
}

size_t ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__size_function__ACFTelem__error_messages(
  const void * untyped_member)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return member->size;
}

const void * ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__get_const_function__ACFTelem__error_messages(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void * ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__get_function__ACFTelem__error_messages(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__fetch_function__ACFTelem__error_messages(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const rosidl_runtime_c__String * item =
    ((const rosidl_runtime_c__String *)
    ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__get_const_function__ACFTelem__error_messages(untyped_member, index));
  rosidl_runtime_c__String * value =
    (rosidl_runtime_c__String *)(untyped_value);
  *value = *item;
}

void ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__assign_function__ACFTelem__error_messages(
  void * untyped_member, size_t index, const void * untyped_value)
{
  rosidl_runtime_c__String * item =
    ((rosidl_runtime_c__String *)
    ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__get_function__ACFTelem__error_messages(untyped_member, index));
  const rosidl_runtime_c__String * value =
    (const rosidl_runtime_c__String *)(untyped_value);
  *item = *value;
}

bool ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__resize_function__ACFTelem__error_messages(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  rosidl_runtime_c__String__Sequence__fini(member);
  return rosidl_runtime_c__String__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__ACFTelem_message_member_array[7] = {
  {
    "id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(ferrobotics__msg__ACFTelem, id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "force",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(ferrobotics__msg__ACFTelem, force),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "position",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(ferrobotics__msg__ACFTelem, position),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "in_contact",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(ferrobotics__msg__ACFTelem, in_contact),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "in_error",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(ferrobotics__msg__ACFTelem, in_error),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "errors",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    8,  // array size
    false,  // is upper bound
    offsetof(ferrobotics__msg__ACFTelem, errors),  // bytes offset in struct
    NULL,  // default value
    ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__size_function__ACFTelem__errors,  // size() function pointer
    ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__get_const_function__ACFTelem__errors,  // get_const(index) function pointer
    ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__get_function__ACFTelem__errors,  // get(index) function pointer
    ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__fetch_function__ACFTelem__errors,  // fetch(index, &value) function pointer
    ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__assign_function__ACFTelem__errors,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "error_messages",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(ferrobotics__msg__ACFTelem, error_messages),  // bytes offset in struct
    NULL,  // default value
    ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__size_function__ACFTelem__error_messages,  // size() function pointer
    ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__get_const_function__ACFTelem__error_messages,  // get_const(index) function pointer
    ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__get_function__ACFTelem__error_messages,  // get(index) function pointer
    ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__fetch_function__ACFTelem__error_messages,  // fetch(index, &value) function pointer
    ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__assign_function__ACFTelem__error_messages,  // assign(index, value) function pointer
    ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__resize_function__ACFTelem__error_messages  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__ACFTelem_message_members = {
  "ferrobotics__msg",  // message namespace
  "ACFTelem",  // message name
  7,  // number of fields
  sizeof(ferrobotics__msg__ACFTelem),
  ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__ACFTelem_message_member_array,  // message members
  ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__ACFTelem_init_function,  // function to initialize message memory (memory has to be allocated)
  ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__ACFTelem_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__ACFTelem_message_type_support_handle = {
  0,
  &ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__ACFTelem_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_ferrobotics
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, ferrobotics, msg, ACFTelem)() {
  if (!ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__ACFTelem_message_type_support_handle.typesupport_identifier) {
    ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__ACFTelem_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &ferrobotics__msg__ACFTelem__rosidl_typesupport_introspection_c__ACFTelem_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
