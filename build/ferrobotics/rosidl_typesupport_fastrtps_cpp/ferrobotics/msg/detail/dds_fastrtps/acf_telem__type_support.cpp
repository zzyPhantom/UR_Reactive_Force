// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from ferrobotics:msg/ACFTelem.idl
// generated code does not contain a copyright notice
#include "ferrobotics/msg/detail/acf_telem__rosidl_typesupport_fastrtps_cpp.hpp"
#include "ferrobotics/msg/detail/acf_telem__struct.hpp"

#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace ferrobotics
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_ferrobotics
cdr_serialize(
  const ferrobotics::msg::ACFTelem & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: id
  cdr << ros_message.id;
  // Member: force
  cdr << ros_message.force;
  // Member: position
  cdr << ros_message.position;
  // Member: in_contact
  cdr << (ros_message.in_contact ? true : false);
  // Member: in_error
  cdr << (ros_message.in_error ? true : false);
  // Member: errors
  {
    cdr << ros_message.errors;
  }
  // Member: error_messages
  {
    cdr << ros_message.error_messages;
  }
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_ferrobotics
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  ferrobotics::msg::ACFTelem & ros_message)
{
  // Member: id
  cdr >> ros_message.id;

  // Member: force
  cdr >> ros_message.force;

  // Member: position
  cdr >> ros_message.position;

  // Member: in_contact
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message.in_contact = tmp ? true : false;
  }

  // Member: in_error
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message.in_error = tmp ? true : false;
  }

  // Member: errors
  {
    cdr >> ros_message.errors;
  }

  // Member: error_messages
  {
    cdr >> ros_message.error_messages;
  }

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_ferrobotics
get_serialized_size(
  const ferrobotics::msg::ACFTelem & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: id
  {
    size_t item_size = sizeof(ros_message.id);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: force
  {
    size_t item_size = sizeof(ros_message.force);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: position
  {
    size_t item_size = sizeof(ros_message.position);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: in_contact
  {
    size_t item_size = sizeof(ros_message.in_contact);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: in_error
  {
    size_t item_size = sizeof(ros_message.in_error);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: errors
  {
    size_t array_size = 8;
    size_t item_size = sizeof(ros_message.errors[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: error_messages
  {
    size_t array_size = ros_message.error_messages.size();

    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        (ros_message.error_messages[index].size() + 1);
    }
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_ferrobotics
max_serialized_size_ACFTelem(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;


  // Member: id
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: force
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: position
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: in_contact
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: in_error
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: errors
  {
    size_t array_size = 8;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: error_messages
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = ferrobotics::msg::ACFTelem;
    is_plain =
      (
      offsetof(DataType, error_messages) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _ACFTelem__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const ferrobotics::msg::ACFTelem *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _ACFTelem__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<ferrobotics::msg::ACFTelem *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _ACFTelem__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const ferrobotics::msg::ACFTelem *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _ACFTelem__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_ACFTelem(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _ACFTelem__callbacks = {
  "ferrobotics::msg",
  "ACFTelem",
  _ACFTelem__cdr_serialize,
  _ACFTelem__cdr_deserialize,
  _ACFTelem__get_serialized_size,
  _ACFTelem__max_serialized_size
};

static rosidl_message_type_support_t _ACFTelem__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_ACFTelem__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace ferrobotics

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_ferrobotics
const rosidl_message_type_support_t *
get_message_type_support_handle<ferrobotics::msg::ACFTelem>()
{
  return &ferrobotics::msg::typesupport_fastrtps_cpp::_ACFTelem__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, ferrobotics, msg, ACFTelem)() {
  return &ferrobotics::msg::typesupport_fastrtps_cpp::_ACFTelem__handle;
}

#ifdef __cplusplus
}
#endif
