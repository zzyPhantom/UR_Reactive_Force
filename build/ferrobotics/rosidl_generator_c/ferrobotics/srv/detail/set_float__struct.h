// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from ferrobotics:srv/SetFloat.idl
// generated code does not contain a copyright notice

#ifndef FERROBOTICS__SRV__DETAIL__SET_FLOAT__STRUCT_H_
#define FERROBOTICS__SRV__DETAIL__SET_FLOAT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/SetFloat in the package ferrobotics.
typedef struct ferrobotics__srv__SetFloat_Request
{
  float value;
} ferrobotics__srv__SetFloat_Request;

// Struct for a sequence of ferrobotics__srv__SetFloat_Request.
typedef struct ferrobotics__srv__SetFloat_Request__Sequence
{
  ferrobotics__srv__SetFloat_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} ferrobotics__srv__SetFloat_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/SetFloat in the package ferrobotics.
typedef struct ferrobotics__srv__SetFloat_Response
{
  bool success;
  rosidl_runtime_c__String message;
} ferrobotics__srv__SetFloat_Response;

// Struct for a sequence of ferrobotics__srv__SetFloat_Response.
typedef struct ferrobotics__srv__SetFloat_Response__Sequence
{
  ferrobotics__srv__SetFloat_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} ferrobotics__srv__SetFloat_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // FERROBOTICS__SRV__DETAIL__SET_FLOAT__STRUCT_H_
