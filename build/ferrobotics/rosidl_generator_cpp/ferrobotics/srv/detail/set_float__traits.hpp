// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from ferrobotics:srv/SetFloat.idl
// generated code does not contain a copyright notice

#ifndef FERROBOTICS__SRV__DETAIL__SET_FLOAT__TRAITS_HPP_
#define FERROBOTICS__SRV__DETAIL__SET_FLOAT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "ferrobotics/srv/detail/set_float__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace ferrobotics
{

namespace srv
{

inline void to_flow_style_yaml(
  const SetFloat_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: value
  {
    out << "value: ";
    rosidl_generator_traits::value_to_yaml(msg.value, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SetFloat_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: value
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "value: ";
    rosidl_generator_traits::value_to_yaml(msg.value, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SetFloat_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace ferrobotics

namespace rosidl_generator_traits
{

[[deprecated("use ferrobotics::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const ferrobotics::srv::SetFloat_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  ferrobotics::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use ferrobotics::srv::to_yaml() instead")]]
inline std::string to_yaml(const ferrobotics::srv::SetFloat_Request & msg)
{
  return ferrobotics::srv::to_yaml(msg);
}

template<>
inline const char * data_type<ferrobotics::srv::SetFloat_Request>()
{
  return "ferrobotics::srv::SetFloat_Request";
}

template<>
inline const char * name<ferrobotics::srv::SetFloat_Request>()
{
  return "ferrobotics/srv/SetFloat_Request";
}

template<>
struct has_fixed_size<ferrobotics::srv::SetFloat_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<ferrobotics::srv::SetFloat_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<ferrobotics::srv::SetFloat_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace ferrobotics
{

namespace srv
{

inline void to_flow_style_yaml(
  const SetFloat_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SetFloat_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SetFloat_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace ferrobotics

namespace rosidl_generator_traits
{

[[deprecated("use ferrobotics::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const ferrobotics::srv::SetFloat_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  ferrobotics::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use ferrobotics::srv::to_yaml() instead")]]
inline std::string to_yaml(const ferrobotics::srv::SetFloat_Response & msg)
{
  return ferrobotics::srv::to_yaml(msg);
}

template<>
inline const char * data_type<ferrobotics::srv::SetFloat_Response>()
{
  return "ferrobotics::srv::SetFloat_Response";
}

template<>
inline const char * name<ferrobotics::srv::SetFloat_Response>()
{
  return "ferrobotics/srv/SetFloat_Response";
}

template<>
struct has_fixed_size<ferrobotics::srv::SetFloat_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<ferrobotics::srv::SetFloat_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<ferrobotics::srv::SetFloat_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<ferrobotics::srv::SetFloat>()
{
  return "ferrobotics::srv::SetFloat";
}

template<>
inline const char * name<ferrobotics::srv::SetFloat>()
{
  return "ferrobotics/srv/SetFloat";
}

template<>
struct has_fixed_size<ferrobotics::srv::SetFloat>
  : std::integral_constant<
    bool,
    has_fixed_size<ferrobotics::srv::SetFloat_Request>::value &&
    has_fixed_size<ferrobotics::srv::SetFloat_Response>::value
  >
{
};

template<>
struct has_bounded_size<ferrobotics::srv::SetFloat>
  : std::integral_constant<
    bool,
    has_bounded_size<ferrobotics::srv::SetFloat_Request>::value &&
    has_bounded_size<ferrobotics::srv::SetFloat_Response>::value
  >
{
};

template<>
struct is_service<ferrobotics::srv::SetFloat>
  : std::true_type
{
};

template<>
struct is_service_request<ferrobotics::srv::SetFloat_Request>
  : std::true_type
{
};

template<>
struct is_service_response<ferrobotics::srv::SetFloat_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // FERROBOTICS__SRV__DETAIL__SET_FLOAT__TRAITS_HPP_
