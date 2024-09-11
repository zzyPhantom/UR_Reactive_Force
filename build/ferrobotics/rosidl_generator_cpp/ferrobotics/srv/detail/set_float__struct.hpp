// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from ferrobotics:srv/SetFloat.idl
// generated code does not contain a copyright notice

#ifndef FERROBOTICS__SRV__DETAIL__SET_FLOAT__STRUCT_HPP_
#define FERROBOTICS__SRV__DETAIL__SET_FLOAT__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__ferrobotics__srv__SetFloat_Request __attribute__((deprecated))
#else
# define DEPRECATED__ferrobotics__srv__SetFloat_Request __declspec(deprecated)
#endif

namespace ferrobotics
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct SetFloat_Request_
{
  using Type = SetFloat_Request_<ContainerAllocator>;

  explicit SetFloat_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->value = 0.0f;
    }
  }

  explicit SetFloat_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->value = 0.0f;
    }
  }

  // field types and members
  using _value_type =
    float;
  _value_type value;

  // setters for named parameter idiom
  Type & set__value(
    const float & _arg)
  {
    this->value = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    ferrobotics::srv::SetFloat_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const ferrobotics::srv::SetFloat_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<ferrobotics::srv::SetFloat_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<ferrobotics::srv::SetFloat_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      ferrobotics::srv::SetFloat_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<ferrobotics::srv::SetFloat_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      ferrobotics::srv::SetFloat_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<ferrobotics::srv::SetFloat_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<ferrobotics::srv::SetFloat_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<ferrobotics::srv::SetFloat_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__ferrobotics__srv__SetFloat_Request
    std::shared_ptr<ferrobotics::srv::SetFloat_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__ferrobotics__srv__SetFloat_Request
    std::shared_ptr<ferrobotics::srv::SetFloat_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SetFloat_Request_ & other) const
  {
    if (this->value != other.value) {
      return false;
    }
    return true;
  }
  bool operator!=(const SetFloat_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SetFloat_Request_

// alias to use template instance with default allocator
using SetFloat_Request =
  ferrobotics::srv::SetFloat_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace ferrobotics


#ifndef _WIN32
# define DEPRECATED__ferrobotics__srv__SetFloat_Response __attribute__((deprecated))
#else
# define DEPRECATED__ferrobotics__srv__SetFloat_Response __declspec(deprecated)
#endif

namespace ferrobotics
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct SetFloat_Response_
{
  using Type = SetFloat_Response_<ContainerAllocator>;

  explicit SetFloat_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  explicit SetFloat_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    ferrobotics::srv::SetFloat_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const ferrobotics::srv::SetFloat_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<ferrobotics::srv::SetFloat_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<ferrobotics::srv::SetFloat_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      ferrobotics::srv::SetFloat_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<ferrobotics::srv::SetFloat_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      ferrobotics::srv::SetFloat_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<ferrobotics::srv::SetFloat_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<ferrobotics::srv::SetFloat_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<ferrobotics::srv::SetFloat_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__ferrobotics__srv__SetFloat_Response
    std::shared_ptr<ferrobotics::srv::SetFloat_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__ferrobotics__srv__SetFloat_Response
    std::shared_ptr<ferrobotics::srv::SetFloat_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SetFloat_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    return true;
  }
  bool operator!=(const SetFloat_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SetFloat_Response_

// alias to use template instance with default allocator
using SetFloat_Response =
  ferrobotics::srv::SetFloat_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace ferrobotics

namespace ferrobotics
{

namespace srv
{

struct SetFloat
{
  using Request = ferrobotics::srv::SetFloat_Request;
  using Response = ferrobotics::srv::SetFloat_Response;
};

}  // namespace srv

}  // namespace ferrobotics

#endif  // FERROBOTICS__SRV__DETAIL__SET_FLOAT__STRUCT_HPP_
