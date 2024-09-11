// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from ferrobotics:srv/SetDuration.idl
// generated code does not contain a copyright notice

#ifndef FERROBOTICS__SRV__DETAIL__SET_DURATION__FUNCTIONS_H_
#define FERROBOTICS__SRV__DETAIL__SET_DURATION__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "ferrobotics/msg/rosidl_generator_c__visibility_control.h"

#include "ferrobotics/srv/detail/set_duration__struct.h"

/// Initialize srv/SetDuration message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * ferrobotics__srv__SetDuration_Request
 * )) before or use
 * ferrobotics__srv__SetDuration_Request__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_ferrobotics
bool
ferrobotics__srv__SetDuration_Request__init(ferrobotics__srv__SetDuration_Request * msg);

/// Finalize srv/SetDuration message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_ferrobotics
void
ferrobotics__srv__SetDuration_Request__fini(ferrobotics__srv__SetDuration_Request * msg);

/// Create srv/SetDuration message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * ferrobotics__srv__SetDuration_Request__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_ferrobotics
ferrobotics__srv__SetDuration_Request *
ferrobotics__srv__SetDuration_Request__create();

/// Destroy srv/SetDuration message.
/**
 * It calls
 * ferrobotics__srv__SetDuration_Request__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_ferrobotics
void
ferrobotics__srv__SetDuration_Request__destroy(ferrobotics__srv__SetDuration_Request * msg);

/// Check for srv/SetDuration message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_ferrobotics
bool
ferrobotics__srv__SetDuration_Request__are_equal(const ferrobotics__srv__SetDuration_Request * lhs, const ferrobotics__srv__SetDuration_Request * rhs);

/// Copy a srv/SetDuration message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_ferrobotics
bool
ferrobotics__srv__SetDuration_Request__copy(
  const ferrobotics__srv__SetDuration_Request * input,
  ferrobotics__srv__SetDuration_Request * output);

/// Initialize array of srv/SetDuration messages.
/**
 * It allocates the memory for the number of elements and calls
 * ferrobotics__srv__SetDuration_Request__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_ferrobotics
bool
ferrobotics__srv__SetDuration_Request__Sequence__init(ferrobotics__srv__SetDuration_Request__Sequence * array, size_t size);

/// Finalize array of srv/SetDuration messages.
/**
 * It calls
 * ferrobotics__srv__SetDuration_Request__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_ferrobotics
void
ferrobotics__srv__SetDuration_Request__Sequence__fini(ferrobotics__srv__SetDuration_Request__Sequence * array);

/// Create array of srv/SetDuration messages.
/**
 * It allocates the memory for the array and calls
 * ferrobotics__srv__SetDuration_Request__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_ferrobotics
ferrobotics__srv__SetDuration_Request__Sequence *
ferrobotics__srv__SetDuration_Request__Sequence__create(size_t size);

/// Destroy array of srv/SetDuration messages.
/**
 * It calls
 * ferrobotics__srv__SetDuration_Request__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_ferrobotics
void
ferrobotics__srv__SetDuration_Request__Sequence__destroy(ferrobotics__srv__SetDuration_Request__Sequence * array);

/// Check for srv/SetDuration message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_ferrobotics
bool
ferrobotics__srv__SetDuration_Request__Sequence__are_equal(const ferrobotics__srv__SetDuration_Request__Sequence * lhs, const ferrobotics__srv__SetDuration_Request__Sequence * rhs);

/// Copy an array of srv/SetDuration messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_ferrobotics
bool
ferrobotics__srv__SetDuration_Request__Sequence__copy(
  const ferrobotics__srv__SetDuration_Request__Sequence * input,
  ferrobotics__srv__SetDuration_Request__Sequence * output);

/// Initialize srv/SetDuration message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * ferrobotics__srv__SetDuration_Response
 * )) before or use
 * ferrobotics__srv__SetDuration_Response__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_ferrobotics
bool
ferrobotics__srv__SetDuration_Response__init(ferrobotics__srv__SetDuration_Response * msg);

/// Finalize srv/SetDuration message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_ferrobotics
void
ferrobotics__srv__SetDuration_Response__fini(ferrobotics__srv__SetDuration_Response * msg);

/// Create srv/SetDuration message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * ferrobotics__srv__SetDuration_Response__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_ferrobotics
ferrobotics__srv__SetDuration_Response *
ferrobotics__srv__SetDuration_Response__create();

/// Destroy srv/SetDuration message.
/**
 * It calls
 * ferrobotics__srv__SetDuration_Response__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_ferrobotics
void
ferrobotics__srv__SetDuration_Response__destroy(ferrobotics__srv__SetDuration_Response * msg);

/// Check for srv/SetDuration message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_ferrobotics
bool
ferrobotics__srv__SetDuration_Response__are_equal(const ferrobotics__srv__SetDuration_Response * lhs, const ferrobotics__srv__SetDuration_Response * rhs);

/// Copy a srv/SetDuration message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_ferrobotics
bool
ferrobotics__srv__SetDuration_Response__copy(
  const ferrobotics__srv__SetDuration_Response * input,
  ferrobotics__srv__SetDuration_Response * output);

/// Initialize array of srv/SetDuration messages.
/**
 * It allocates the memory for the number of elements and calls
 * ferrobotics__srv__SetDuration_Response__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_ferrobotics
bool
ferrobotics__srv__SetDuration_Response__Sequence__init(ferrobotics__srv__SetDuration_Response__Sequence * array, size_t size);

/// Finalize array of srv/SetDuration messages.
/**
 * It calls
 * ferrobotics__srv__SetDuration_Response__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_ferrobotics
void
ferrobotics__srv__SetDuration_Response__Sequence__fini(ferrobotics__srv__SetDuration_Response__Sequence * array);

/// Create array of srv/SetDuration messages.
/**
 * It allocates the memory for the array and calls
 * ferrobotics__srv__SetDuration_Response__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_ferrobotics
ferrobotics__srv__SetDuration_Response__Sequence *
ferrobotics__srv__SetDuration_Response__Sequence__create(size_t size);

/// Destroy array of srv/SetDuration messages.
/**
 * It calls
 * ferrobotics__srv__SetDuration_Response__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_ferrobotics
void
ferrobotics__srv__SetDuration_Response__Sequence__destroy(ferrobotics__srv__SetDuration_Response__Sequence * array);

/// Check for srv/SetDuration message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_ferrobotics
bool
ferrobotics__srv__SetDuration_Response__Sequence__are_equal(const ferrobotics__srv__SetDuration_Response__Sequence * lhs, const ferrobotics__srv__SetDuration_Response__Sequence * rhs);

/// Copy an array of srv/SetDuration messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_ferrobotics
bool
ferrobotics__srv__SetDuration_Response__Sequence__copy(
  const ferrobotics__srv__SetDuration_Response__Sequence * input,
  ferrobotics__srv__SetDuration_Response__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // FERROBOTICS__SRV__DETAIL__SET_DURATION__FUNCTIONS_H_
