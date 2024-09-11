// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from ferrobotics:msg/ACFTelem.idl
// generated code does not contain a copyright notice

#ifndef FERROBOTICS__MSG__DETAIL__ACF_TELEM__BUILDER_HPP_
#define FERROBOTICS__MSG__DETAIL__ACF_TELEM__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "ferrobotics/msg/detail/acf_telem__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace ferrobotics
{

namespace msg
{

namespace builder
{

class Init_ACFTelem_error_messages
{
public:
  explicit Init_ACFTelem_error_messages(::ferrobotics::msg::ACFTelem & msg)
  : msg_(msg)
  {}
  ::ferrobotics::msg::ACFTelem error_messages(::ferrobotics::msg::ACFTelem::_error_messages_type arg)
  {
    msg_.error_messages = std::move(arg);
    return std::move(msg_);
  }

private:
  ::ferrobotics::msg::ACFTelem msg_;
};

class Init_ACFTelem_errors
{
public:
  explicit Init_ACFTelem_errors(::ferrobotics::msg::ACFTelem & msg)
  : msg_(msg)
  {}
  Init_ACFTelem_error_messages errors(::ferrobotics::msg::ACFTelem::_errors_type arg)
  {
    msg_.errors = std::move(arg);
    return Init_ACFTelem_error_messages(msg_);
  }

private:
  ::ferrobotics::msg::ACFTelem msg_;
};

class Init_ACFTelem_in_error
{
public:
  explicit Init_ACFTelem_in_error(::ferrobotics::msg::ACFTelem & msg)
  : msg_(msg)
  {}
  Init_ACFTelem_errors in_error(::ferrobotics::msg::ACFTelem::_in_error_type arg)
  {
    msg_.in_error = std::move(arg);
    return Init_ACFTelem_errors(msg_);
  }

private:
  ::ferrobotics::msg::ACFTelem msg_;
};

class Init_ACFTelem_in_contact
{
public:
  explicit Init_ACFTelem_in_contact(::ferrobotics::msg::ACFTelem & msg)
  : msg_(msg)
  {}
  Init_ACFTelem_in_error in_contact(::ferrobotics::msg::ACFTelem::_in_contact_type arg)
  {
    msg_.in_contact = std::move(arg);
    return Init_ACFTelem_in_error(msg_);
  }

private:
  ::ferrobotics::msg::ACFTelem msg_;
};

class Init_ACFTelem_position
{
public:
  explicit Init_ACFTelem_position(::ferrobotics::msg::ACFTelem & msg)
  : msg_(msg)
  {}
  Init_ACFTelem_in_contact position(::ferrobotics::msg::ACFTelem::_position_type arg)
  {
    msg_.position = std::move(arg);
    return Init_ACFTelem_in_contact(msg_);
  }

private:
  ::ferrobotics::msg::ACFTelem msg_;
};

class Init_ACFTelem_force
{
public:
  explicit Init_ACFTelem_force(::ferrobotics::msg::ACFTelem & msg)
  : msg_(msg)
  {}
  Init_ACFTelem_position force(::ferrobotics::msg::ACFTelem::_force_type arg)
  {
    msg_.force = std::move(arg);
    return Init_ACFTelem_position(msg_);
  }

private:
  ::ferrobotics::msg::ACFTelem msg_;
};

class Init_ACFTelem_id
{
public:
  Init_ACFTelem_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ACFTelem_force id(::ferrobotics::msg::ACFTelem::_id_type arg)
  {
    msg_.id = std::move(arg);
    return Init_ACFTelem_force(msg_);
  }

private:
  ::ferrobotics::msg::ACFTelem msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::ferrobotics::msg::ACFTelem>()
{
  return ferrobotics::msg::builder::Init_ACFTelem_id();
}

}  // namespace ferrobotics

#endif  // FERROBOTICS__MSG__DETAIL__ACF_TELEM__BUILDER_HPP_
