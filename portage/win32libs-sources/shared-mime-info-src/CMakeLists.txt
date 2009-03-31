# This script compiles update-mime-database on windows
# needed libs:
# libxml2 >= 2.6
# libintl >= 0.14
# iconv

# additionally you'll need the following sources
# shared-mimeinfo
# kdewin32
# glib >= 2.12
# extract all into on directory and adjust the following paths:

project(update-mime-database)
cmake_minimum_required(VERSION 2.6.2)
set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}")

if(COMMAND cmake_policy)
  cmake_policy(SET CMP0003 NEW)
endif(COMMAND cmake_policy)

include(CheckIncludeFiles)
include(CheckSymbolExists)

set(KDEWIN32_DIR "" CACHE FILEPATH "Path to kdewin32 sources")
set(GLIB_DIR     "" CACHE FILEPATH "Path to glib sources")

# libxml2
find_package(LIBXML2 REQUIRED)
# libintl
find_package(Libintl REQUIRED)

# configure checks
check_include_files(inttypes.h  HAVE_INTTYPES_H)
check_include_files(locale.h    HAVE_LOCALE_H)
check_include_files(memory.h    HAVE_MEMORY_H)
check_include_files(stdint.h    HAVE_STDINT_H)
check_include_files(stdlib.h    HAVE_STDLIB_H)
check_include_files(strings.h   HAVE_STRINGS_H)
check_include_files(string.h    HAVE_STRING_H)
check_include_files(sys/stat.h  HAVE_SYS_STAT_H)
check_include_files(sys/types.h HAVE_SYS_TYPES_H)
check_include_files(unistd.h    HAVE_UNISTD_H)
check_symbol_exists(LC_MESSAGES locale.h HAVE_LC_MESSAGES)

set(PACKAGE           "update-mime-database")
set(PACKAGE_BUGREPORT "https://bugs.freedesktop.org/enter_bug.cgi?product=shared-mime-info")
set(PACKAGE_NAME      "shared-mime-info")
set(PACKAGE_STRING    "shared-mime-info 0.60")
set(PACKAGE_TARNAME   "shared-mime-info")
set(PACKAGE_VERSION   "0.60")
set(VERSION           "0.60")
configure_file(${CMAKE_SOURCE_DIR}/config.h.cmake ${CMAKE_BINARY_DIR}/config.h)

set(GLIB_SOURCES
    ${GLIB_DIR}/glib/galiasdef.c
    ${GLIB_DIR}/glib/gatomic.c
    ${GLIB_DIR}/glib/garray.c
    ${GLIB_DIR}/glib/gconvert.c
    ${GLIB_DIR}/glib/gdataset.c
    ${GLIB_DIR}/glib/gerror.c
    ${GLIB_DIR}/glib/gfileutils.c
    ${GLIB_DIR}/glib/ghash.c
    ${GLIB_DIR}/glib/glist.c
    ${GLIB_DIR}/glib/gmain.c
    ${GLIB_DIR}/glib/gmem.c
    ${GLIB_DIR}/glib/gmessages.c
    ${GLIB_DIR}/glib/gprimes.c
    ${GLIB_DIR}/glib/gprintf.c
    ${GLIB_DIR}/glib/gqsort.c
    ${GLIB_DIR}/glib/grand.c
    ${GLIB_DIR}/glib/gutf8.c
    ${GLIB_DIR}/glib/gutils.c
    ${GLIB_DIR}/glib/gstdio.c
    ${GLIB_DIR}/glib/gslice.c
    ${GLIB_DIR}/glib/gslist.c
    ${GLIB_DIR}/glib/gstrfuncs.c
    ${GLIB_DIR}/glib/gstring.c
    ${GLIB_DIR}/glib/gtestutils.c
    ${GLIB_DIR}/glib/gthread.c
    ${GLIB_DIR}/glib/gtimer.c
    ${GLIB_DIR}/glib/guniprop.c
    ${GLIB_DIR}/glib/gunidecomp.c
    ${GLIB_DIR}/glib/gwin32.c
    ${GLIB_DIR}/glib/gnulib/printf.c
    ${GLIB_DIR}/glib/gnulib/printf-args.c
    ${GLIB_DIR}/glib/gnulib/printf-parse.c
    ${GLIB_DIR}/glib/gnulib/vasnprintf.c
    ${GLIB_DIR}/glib/libcharset/localcharset.c
)

include_directories(
   ${GLIB_DIR}
   ${GLIB_DIR}/glib
   ${LIBINTL_INCLUDE_DIR}
   ${KDEWIN32_DIR}/include
   ${LIBXML2_INCLUDE_DIR}
   ${CMAKE_BINARY_DIR}
)

if(MSVC)
  include_directories(
     ${KDEWIN32_DIR}/include/msvc
   )
endif(MSVC)
if(MINGW)
  include_directories(
     ${KDEWIN32_DIR}/include/mingw
   )
endif(MINGW)

if(MSVC)
  add_definitions( -D_CRT_SECURE_NO_DEPRECATE -D_CRT_NONSTDC_NO_DEPRECATE -wd4018)
  set(additional_SOURCES ${KDEWIN32_DIR}/src/dirent.c ${KDEWIN32_DIR}/src/unistd.c)
endif(MSVC)

add_definitions(-DGLIB_VAR= -DWINPOSIX_EXPORT= -DWIN32_LEAN_AND_MEAN -DG_DISABLE_DEPRECATED -DLIBDIR=\"lib\")

add_executable(update-mime-database update-mime-database.c ${GLIB_SOURCES} ${additional_SOURCES})

target_link_libraries(update-mime-database
        ${LIBINTL_LIBRARIES}
        ${LIBXML2_LIBRARIES}
        ole32
)

install(TARGETS update-mime-database RUNTIME DESTINATION bin)
install(FILES ${CMAKE_SOURCE_DIR}/freedesktop.org.xml DESTINATION share/mime/packages)
