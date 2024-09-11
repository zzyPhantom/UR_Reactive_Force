// generated from rosidl_typesupport_c/resource/idl__type_support.cpp.em
// with input from ferrobotics:srv/SetDuration.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "ferrobotics/srv/detail/set_duration__struct.h"
#include "ferrobotics/srv/detail/set_duration__type_support.h"
#include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/message_type_support_dispatch.h"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_c/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace ferrobotics
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _SetDuration_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _SetDuration_Request_type_support_ids_t;

static const _SetDuration_Request_type_support_ids_t _SetDuration_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _SetDuration_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _SetDuration_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _SetDuration_Request_type_support_symbol_names_t _SetDuration_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, ferrobotics, srv, SetDuration_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, ferrobotics, srv, SetDuration_Request)),
  }
};

typedef struct _SetDuration_Request_type_support_data_t
{
  void * data[2];
} _SetDuration_Request_type_support_data_t;

static _SetDuration_Request_type_support_data_t _SetDuration_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _SetDuration_Request_message_typesupport_map = {
  2,
  "ferrobotics",
  &_SetDuration_Request_message_typesupport_ids.typesupport_identifier[0],
  &_SetDuration_Request_message_typesupport_symbol_names.symbol_name[0],
  &_SetDuration_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t SetDuration_Request_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_SetDuration_Request_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace ferrobotics

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, ferrobotics, srv, SetDuration_Request)() {
  return &::ferrobotics::srv::rosidl_typesupport_c::SetDuration_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "ferrobotics/srv/detail/set_duration__struct.h"
// already included above
// #include "ferrobotics/srv/detail/set_duration__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace ferrobotics
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _SetDuration_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _SetDuration_Response_type_support_ids_t;

static const _SetDuration_Response_type_support_ids_t _SetDuration_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _SetDuration_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _SetDuration_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _SetDuration_Response_type_support_symbol_names_t _SetDuration_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, ferrobotics, srv, SetDuration_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, ferrobotics, srv, SetDuration_Response)),
  }
};

typedef struct _SetDuration_Response_type_support_data_t
{
  void * data[2];
} _SetDuration_Response_type_support_data_t;

static _SetDuration_Response_type_support_data_t _SetDuration_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _SetDuration_Response_message_typesupport_map = {
  2,
  "ferrobotics",
  &_SetDuration_Response_message_typesupport_ids.typesupport_identifier[0],
  &_SetDuration_Response_message_typesupport_symbol_names.symbol_name[0],
  &_SetDuration_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t SetDuration_Response_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_SetDuration_Response_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace ferrobotics

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, ferrobotics, srv, SetDuration_Response)() {
  return &::ferrobotics::srv::rosidl_typesupport_c::SetDuration_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "ferrobotics/srv/detail/set_duration__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/service_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace ferrobotics
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _SetDuration_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _SetDuration_type_support_ids_t;

static const _SetDuration_type_support_ids_t _SetDuration_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _SetDuration_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _SetDuration_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _SetDuration_type_support_symbol_names_t _SetDuration_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, ferrobotics, srv, SetDuration)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, ferrobotics, srv, SetDuration)),
  }
};

typedef struct _SetDuration_type_support_data_t
{
  void * data[2];
} _SetDuration_type_support_data_t;

static _SetDuration_type_support_data_t _SetDuration_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _SetDuration_service_typesupport_map = {
  2,
  "ferrobotics",
  &_SetDuration_service_typesupport_ids.typesupport_identifier[0],
  &_SetDuration_service_typesupport_symbol_names.symbol_name[0],
  &_SetDuration_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t SetDuration_service_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_SetDuration_service_typesupport_map),
  rosidl_typesupport_c__get_service_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace ferrobotics

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_c, ferrobotics, srv, SetDuration)() {
  return &::ferrobotics::srv::rosidl_typesupport_c::SetDuration_service_type_support_handle;
}

#ifdef __cplusplus
}
#endif
