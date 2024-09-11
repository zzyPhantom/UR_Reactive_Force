// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from ferrobotics:msg/ACFTelem.idl
// generated code does not contain a copyright notice

#ifndef FERROBOTICS__MSG__DETAIL__ACF_TELEM__STRUCT_H_
#define FERROBOTICS__MSG__DETAIL__ACF_TELEM__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'error_messages'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/ACFTelem in the package ferrobotics.
typedef struct ferrobotics__msg__ACFTelem
{
  int32_t id;
  float force;
  float position;
  bool in_contact;
  bool in_error;
  bool errors[8];
  rosidl_runtime_c__String__Sequence error_messages;
} ferrobotics__msg__ACFTelem;

// Struct for a sequence of ferrobotics__msg__ACFTelem.
typedef struct ferrobotics__msg__ACFTelem__Sequence
{
  ferrobotics__msg__ACFTelem * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} ferrobotics__msg__ACFTelem__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // FERROBOTICS__MSG__DETAIL__ACF_TELEM__STRUCT_H_
