# - Try to find the OpenSP library
# 
# Once done this will define
#
#  OPENSP_FOUND - system has OPENSP
#  OPENSP_INCLUDES - the OPENSP include directories
#  OPENSP_LIBRARIES - The libraries needed to use OPENSP

if (WIN32)

    set(OPENSP_FOUND FALSE)
    find_path(OPENSP_INCLUDES ParserEventGeneratorKit.h
        $ENV{KDEROOT}/include/opensp
    )

    find_library(OPENSP_LIBRARIES
        NAMES sp133.lib
        PATHS
            $ENV{KDEROOT}/lib
    )

    if (OPENSP_INCLUDES AND OPENSP_OPENSP_LIBRARIES)
        set(OPENSP_FOUND TRUE)
    endif (OPENSP_INCLUDES AND OPENSP_OPENSP_LIBRARIES)

  if (OPENSP_FOUND)
    if (NOT OPENSP_FIND_QUIETLY)
      message(STATUS "Found OPENSP library: ${OPENSP_LIBRARIES}")
    endif (NOT OPENSP_FIND_QUIETLY)

  else (OPENSP_FOUND)
    if (OPENSP_FIND_REQUIRED)
      message(FATAL_ERROR "Could NOT find OPENSP library\nPlease install it first")
    endif (OPENSP_FIND_REQUIRED)
  endif (OPENSP_FOUND)
endif (WIN32)
