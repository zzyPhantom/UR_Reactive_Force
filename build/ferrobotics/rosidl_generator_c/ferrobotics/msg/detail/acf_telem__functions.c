// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from ferrobotics:msg/ACFTelem.idl
// generated code does not contain a copyright notice
#include "ferrobotics/msg/detail/acf_telem__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `error_messages`
#include "rosidl_runtime_c/string_functions.h"

bool
ferrobotics__msg__ACFTelem__init(ferrobotics__msg__ACFTelem * msg)
{
  if (!msg) {
    return false;
  }
  // id
  // force
  // position
  // in_contact
  // in_error
  // errors
  // error_messages
  if (!rosidl_runtime_c__String__Sequence__init(&msg->error_messages, 0)) {
    ferrobotics__msg__ACFTelem__fini(msg);
    return false;
  }
  return true;
}

void
ferrobotics__msg__ACFTelem__fini(ferrobotics__msg__ACFTelem * msg)
{
  if (!msg) {
    return;
  }
  // id
  // force
  // position
  // in_contact
  // in_error
  // errors
  // error_messages
  rosidl_runtime_c__String__Sequence__fini(&msg->error_messages);
}

bool
ferrobotics__msg__ACFTelem__are_equal(const ferrobotics__msg__ACFTelem * lhs, const ferrobotics__msg__ACFTelem * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // id
  if (lhs->id != rhs->id) {
    return false;
  }
  // force
  if (lhs->force != rhs->force) {
    return false;
  }
  // position
  if (lhs->position != rhs->position) {
    return false;
  }
  // in_contact
  if (lhs->in_contact != rhs->in_contact) {
    return false;
  }
  // in_error
  if (lhs->in_error != rhs->in_error) {
    return false;
  }
  // errors
  for (size_t i = 0; i < 8; ++i) {
    if (lhs->errors[i] != rhs->errors[i]) {
      return false;
    }
  }
  // error_messages
  if (!rosidl_runtime_c__String__Sequence__are_equal(
      &(lhs->error_messages), &(rhs->error_messages)))
  {
    return false;
  }
  return true;
}

bool
ferrobotics__msg__ACFTelem__copy(
  const ferrobotics__msg__ACFTelem * input,
  ferrobotics__msg__ACFTelem * output)
{
  if (!input || !output) {
    return false;
  }
  // id
  output->id = input->id;
  // force
  output->force = input->force;
  // position
  output->position = input->position;
  // in_contact
  output->in_contact = input->in_contact;
  // in_error
  output->in_error = input->in_error;
  // errors
  for (size_t i = 0; i < 8; ++i) {
    output->errors[i] = input->errors[i];
  }
  // error_messages
  if (!rosidl_runtime_c__String__Sequence__copy(
      &(input->error_messages), &(output->error_messages)))
  {
    return false;
  }
  return true;
}

ferrobotics__msg__ACFTelem *
ferrobotics__msg__ACFTelem__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  ferrobotics__msg__ACFTelem * msg = (ferrobotics__msg__ACFTelem *)allocator.allocate(sizeof(ferrobotics__msg__ACFTelem), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(ferrobotics__msg__ACFTelem));
  bool success = ferrobotics__msg__ACFTelem__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
ferrobotics__msg__ACFTelem__destroy(ferrobotics__msg__ACFTelem * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    ferrobotics__msg__ACFTelem__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
ferrobotics__msg__ACFTelem__Sequence__init(ferrobotics__msg__ACFTelem__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  ferrobotics__msg__ACFTelem * data = NULL;

  if (size) {
    data = (ferrobotics__msg__ACFTelem *)allocator.zero_allocate(size, sizeof(ferrobotics__msg__ACFTelem), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = ferrobotics__msg__ACFTelem__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        ferrobotics__msg__ACFTelem__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
ferrobotics__msg__ACFTelem__Sequence__fini(ferrobotics__msg__ACFTelem__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      ferrobotics__msg__ACFTelem__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

ferrobotics__msg__ACFTelem__Sequence *
ferrobotics__msg__ACFTelem__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  ferrobotics__msg__ACFTelem__Sequence * array = (ferrobotics__msg__ACFTelem__Sequence *)allocator.allocate(sizeof(ferrobotics__msg__ACFTelem__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = ferrobotics__msg__ACFTelem__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
ferrobotics__msg__ACFTelem__Sequence__destroy(ferrobotics__msg__ACFTelem__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    ferrobotics__msg__ACFTelem__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
ferrobotics__msg__ACFTelem__Sequence__are_equal(const ferrobotics__msg__ACFTelem__Sequence * lhs, const ferrobotics__msg__ACFTelem__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!ferrobotics__msg__ACFTelem__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
ferrobotics__msg__ACFTelem__Sequence__copy(
  const ferrobotics__msg__ACFTelem__Sequence * input,
  ferrobotics__msg__ACFTelem__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(ferrobotics__msg__ACFTelem);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    ferrobotics__msg__ACFTelem * data =
      (ferrobotics__msg__ACFTelem *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!ferrobotics__msg__ACFTelem__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          ferrobotics__msg__ACFTelem__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!ferrobotics__msg__ACFTelem__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
