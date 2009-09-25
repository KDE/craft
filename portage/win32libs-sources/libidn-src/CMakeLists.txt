project(libidn)
cmake_minimum_required(VERSION 2.6.2)
set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}")

set(PACKAGE "libidn")
set(PACKAGE_NAME "GNU Libidn")
set(PACKAGE_VERSION "1.15")
set(PACKAGE_BUGREPORT "bug-libidn@gnu.org")
set(LOCALEDIR .)

set(libIDN_srcs
  lib/idn-free.c
  lib/idna.c
  lib/nfkc.c
  lib/pr29.c
  lib/profiles.c
  lib/punycode.c
  lib/rfc3454.c
  lib/strerror-idna.c
  lib/strerror-pr29.c
  lib/strerror-punycode.c
  lib/strerror-stringprep.c
  lib/strerror-tld.c
  lib/stringprep.c
  lib/tld.c
  lib/tlds.c
  lib/toutf8.c
  lib/version.c

  lib/gl/c-ctype.c
  lib/gl/c-strcasecmp.c
  lib/gl/c-strncasecmp.c
#  lib/gl/iconv_open.c
#  lib/gl/malloc.c
#  lib/gl/strdup.c
#  lib/gl/striconv.c
  lib/gl/strverscmp.c
)

set(libIDN_hdrs
  lib/idn-free.h
  lib/idna.h
  lib/pr29.h
  lib/punycode.h
  lib/stringprep.h
  lib/tld.h
  ${CMAKE_CURRENT_BINARY_DIR}/idn-int.h
)

set(IDN_srcs
  gl/error.c
  gl/progname.c
  gl/version-etc.c
  src/idn.c
  src/idn_cmd.c
)

add_definitions(-D_CRT_SECURE_NO_DEPRECATE -D_CRT_NONSTDC_NO_DEPRECATE)
add_definitions(-DHAVE_CONFIG_H -DLIBIDN_BUILDING)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/lib)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/lib/gl)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/gl)
if(MSVC)
  include_directories(${CMAKE_CURRENT_SOURCE_DIR}/win32/include)
ENDIF(MSVC)
include_directories(${CMAKE_CURRENT_BINARY_DIR})

configure_file(${CMAKE_CURRENT_SOURCE_DIR}/config.h.cmake ${CMAKE_CURRENT_BINARY_DIR}/config.h)
if(MINGW)
  configure_file(${CMAKE_CURRENT_SOURCE_DIR}/idn-int.h.cmake ${CMAKE_CURRENT_BINARY_DIR}/idn-int.h)
endif(MINGW)

add_library(idn-11 SHARED ${libIDN_srcs})
add_executable(idn ${IDN_srcs})
target_link_libraries(idn idn-11)

install(TARGETS idn-11 idn
                RUNTIME DESTINATION bin
                LIBRARY DESTINATION lib
                ARCHIVE DESTINATION lib
)
install(FILES ${libIDN_hdrs} DESTINATION include)
