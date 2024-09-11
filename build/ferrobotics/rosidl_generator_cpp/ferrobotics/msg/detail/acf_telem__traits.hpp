// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from ferrobotics:msg/ACFTelem.idl
// generated code does not contain a copyright notice

#ifndef FERROBOTICS__MSG__DETAIL__ACF_TELEM__TRAITS_HPP_
#define FERROBOTICS__MSG__DETAIL__ACF_TELEM__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "ferrobotics/msg/detail/acf_telem__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace ferrobotics
{

namespace msg
{

inline void to_flow_style_yaml(
  const ACFTelem & msg,
  std::ostream & out)
{
  out << "{";
  // member: id
  {
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
    out << ", ";
  }

  // member: force
  {
    out << "force: ";
    rosidl_generator_traits::value_to_yaml(msg.force, out);
    out << ", ";
  }

  // member: position
  {
    out << "position: ";
    rosidl_generator_traits::value_to_yaml(msg.position, out);
    out << ", ";
  }

  // member: in_contact
  {
    out << "in_contact: ";
    rosidl_generator_traits::value_to_yaml(msg.in_contact, out);
    out << ", ";
  }

  // member: in_error
  {
    out << "in_error: ";
    rosidl_generator_traits::value_to_yaml(msg.in_error, out);
    out << ", ";
  }

  // member: errors
  {
    if (msg.errors.size() == 0) {
      out << "errors: []";
    } else {
      out << "errors: [";
      size_t pending_items = msg.errors.size();
      for (auto item : msg.errors) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: error_messages
  {
    if (msg.error_messages.size() == 0) {
      out << "error_messages: []";
    } else {
      out << "error_messages: [";
      size_t pending_items = msg.error_messages.size();
      for (auto item : msg.error_messages) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ACFTelem & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
    out << "\n";
  }

  // member: force
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "force: ";
    rosidl_generator_traits::value_to_yaml(msg.force, out);
    out << "\n";
  }

  // member: position
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "position: ";
    rosidl_generator_traits::value_to_yaml(msg.position, out);
    out << "\n";
  }

  // member: in_contact
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "in_contact: ";
    rosidl_generator_traits::value_to_yaml(msg.in_contact, out);
    out << "\n";
  }

  // member: in_error
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "in_error: ";
    rosidl_generator_traits::value_to_yaml(msg.in_error, out);
    out << "\n";
  }

  // member: errors
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.errors.size() == 0) {
      out << "errors: []\n";
    } else {
      out << "errors:\n";
      for (auto item : msg.errors) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: error_messages
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.error_messages.size() == 0) {
      out << "error_messages: []\n";
    } else {
      out << "error_messages:\n";
      for (auto item : msg.error_messages) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ACFTelem & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace ferrobotics

namespace rosidl_generator_traits
{

[[deprecated("use ferrobotics::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const ferrobotics::msg::ACFTelem & msg,
  std::ostream & out, size_t indentation = 0)
{
  ferrobotics::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use ferrobotics::msg::to_yaml() instead")]]
inline std::string to_yaml(const ferrobotics::msg::ACFTelem & msg)
{
  return ferrobotics::msg::to_yaml(msg);
}

template<>
inline const char * data_type<ferrobotics::msg::ACFTelem>()
{
  return "ferrobotics::msg::ACFTelem";
}

template<>
inline const char * name<ferrobotics::msg::ACFTelem>()
{
  return "ferrobotics/msg/ACFTelem";
}

template<>
struct has_fixed_size<ferrobotics::msg::ACFTelem>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<ferrobotics::msg::ACFTelem>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<ferrobotics::msg::ACFTelem>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // FERROBOTICS__MSG__DETAIL__ACF_TELEM__TRAITS_HPP_
