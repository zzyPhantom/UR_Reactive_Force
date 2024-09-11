// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from ferrobotics:msg/ACFTelem.idl
// generated code does not contain a copyright notice

#ifndef FERROBOTICS__MSG__DETAIL__ACF_TELEM__STRUCT_HPP_
#define FERROBOTICS__MSG__DETAIL__ACF_TELEM__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__ferrobotics__msg__ACFTelem __attribute__((deprecated))
#else
# define DEPRECATED__ferrobotics__msg__ACFTelem __declspec(deprecated)
#endif

namespace ferrobotics
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ACFTelem_
{
  using Type = ACFTelem_<ContainerAllocator>;

  explicit ACFTelem_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->id = 0l;
      this->force = 0.0f;
      this->position = 0.0f;
      this->in_contact = false;
      this->in_error = false;
      std::fill<typename std::array<bool, 8>::iterator, bool>(this->errors.begin(), this->errors.end(), false);
    }
  }

  explicit ACFTelem_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : errors(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->id = 0l;
      this->force = 0.0f;
      this->position = 0.0f;
      this->in_contact = false;
      this->in_error = false;
      std::fill<typename std::array<bool, 8>::iterator, bool>(this->errors.begin(), this->errors.end(), false);
    }
  }

  // field types and members
  using _id_type =
    int32_t;
  _id_type id;
  using _force_type =
    float;
  _force_type force;
  using _position_type =
    float;
  _position_type position;
  using _in_contact_type =
    bool;
  _in_contact_type in_contact;
  using _in_error_type =
    bool;
  _in_error_type in_error;
  using _errors_type =
    std::array<bool, 8>;
  _errors_type errors;
  using _error_messages_type =
    std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>>;
  _error_messages_type error_messages;

  // setters for named parameter idiom
  Type & set__id(
    const int32_t & _arg)
  {
    this->id = _arg;
    return *this;
  }
  Type & set__force(
    const float & _arg)
  {
    this->force = _arg;
    return *this;
  }
  Type & set__position(
    const float & _arg)
  {
    this->position = _arg;
    return *this;
  }
  Type & set__in_contact(
    const bool & _arg)
  {
    this->in_contact = _arg;
    return *this;
  }
  Type & set__in_error(
    const bool & _arg)
  {
    this->in_error = _arg;
    return *this;
  }
  Type & set__errors(
    const std::array<bool, 8> & _arg)
  {
    this->errors = _arg;
    return *this;
  }
  Type & set__error_messages(
    const std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>> & _arg)
  {
    this->error_messages = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    ferrobotics::msg::ACFTelem_<ContainerAllocator> *;
  using ConstRawPtr =
    const ferrobotics::msg::ACFTelem_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<ferrobotics::msg::ACFTelem_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<ferrobotics::msg::ACFTelem_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      ferrobotics::msg::ACFTelem_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<ferrobotics::msg::ACFTelem_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      ferrobotics::msg::ACFTelem_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<ferrobotics::msg::ACFTelem_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<ferrobotics::msg::ACFTelem_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<ferrobotics::msg::ACFTelem_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__ferrobotics__msg__ACFTelem
    std::shared_ptr<ferrobotics::msg::ACFTelem_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__ferrobotics__msg__ACFTelem
    std::shared_ptr<ferrobotics::msg::ACFTelem_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ACFTelem_ & other) const
  {
    if (this->id != other.id) {
      return false;
    }
    if (this->force != other.force) {
      return false;
    }
    if (this->position != other.position) {
      return false;
    }
    if (this->in_contact != other.in_contact) {
      return false;
    }
    if (this->in_error != other.in_error) {
      return false;
    }
    if (this->errors != other.errors) {
      return false;
    }
    if (this->error_messages != other.error_messages) {
      return false;
    }
    return true;
  }
  bool operator!=(const ACFTelem_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ACFTelem_

// alias to use template instance with default allocator
using ACFTelem =
  ferrobotics::msg::ACFTelem_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace ferrobotics

#endif  // FERROBOTICS__MSG__DETAIL__ACF_TELEM__STRUCT_HPP_
