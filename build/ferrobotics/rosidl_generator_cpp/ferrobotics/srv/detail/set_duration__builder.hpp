// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from ferrobotics:srv/SetDuration.idl
// generated code does not contain a copyright notice

#ifndef FERROBOTICS__SRV__DETAIL__SET_DURATION__BUILDER_HPP_
#define FERROBOTICS__SRV__DETAIL__SET_DURATION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "ferrobotics/srv/detail/set_duration__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace ferrobotics
{

namespace srv
{

namespace builder
{

class Init_SetDuration_Request_duration
{
public:
  Init_SetDuration_Request_duration()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::ferrobotics::srv::SetDuration_Request duration(::ferrobotics::srv::SetDuration_Request::_duration_type arg)
  {
    msg_.duration = std::move(arg);
    return std::move(msg_);
  }

private:
  ::ferrobotics::srv::SetDuration_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::ferrobotics::srv::SetDuration_Request>()
{
  return ferrobotics::srv::builder::Init_SetDuration_Request_duration();
}

}  // namespace ferrobotics


namespace ferrobotics
{

namespace srv
{

namespace builder
{

class Init_SetDuration_Response_message
{
public:
  explicit Init_SetDuration_Response_message(::ferrobotics::srv::SetDuration_Response & msg)
  : msg_(msg)
  {}
  ::ferrobotics::srv::SetDuration_Response message(::ferrobotics::srv::SetDuration_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::ferrobotics::srv::SetDuration_Response msg_;
};

class Init_SetDuration_Response_success
{
public:
  Init_SetDuration_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SetDuration_Response_message success(::ferrobotics::srv::SetDuration_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_SetDuration_Response_message(msg_);
  }

private:
  ::ferrobotics::srv::SetDuration_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::ferrobotics::srv::SetDuration_Response>()
{
  return ferrobotics::srv::builder::Init_SetDuration_Response_success();
}

}  // namespace ferrobotics

#endif  // FERROBOTICS__SRV__DETAIL__SET_DURATION__BUILDER_HPP_
