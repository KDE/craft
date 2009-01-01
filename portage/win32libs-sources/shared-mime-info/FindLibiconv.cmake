# Try to find LibIconv functionality
# Once done this will define
#
#  LIBICONV_FOUND - system has Libiconv
#  LIBICONV_INCLUDE_DIR - Libiconv include directory
#  LIBICONV_LIBRARIES - Libraries needed to use Libiconv
#

if(LIBICONV_INCLUDE_DIR AND LIBICONV_LIBRARIES)
  set(Libiconv_FIND_QUIETLY TRUE)
endif(LIBICONV_INCLUDE_DIR AND LIBICONV_LIBRARIES)

find_path(LIBICONV_INCLUDE_DIR iconv.h)

find_library(LIBICONV_LIBRARIES iconv)

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(Libiconv  DEFAULT_MSG  LIBICONV_INCLUDE_DIR  LIBICONV_LIBRARIES)

mark_as_advanced(LIBICONV_INCLUDE_DIR LIBICONV_LIBRARIES)
