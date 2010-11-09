
# It also adds the following macros
#  AUTOMOC4(<target> <SRCS_VAR>)
#    Use this to run automoc4 on all files contained in the list <SRCS_VAR>.
#
#  AUTOMOC4_MOC_HEADERS(<target> header1.h header2.h ...)
#    Use this to add more header files to be processed with automoc4.
#
#  AUTOMOC4_ADD_EXECUTABLE(<target_NAME> src1 src2 ...)
#    This macro does the same as ADD_EXECUTABLE, but additionally
#    adds automoc4 handling for all source files.
#
# AUTOMOC4_ADD_LIBRARY(<target_NAME> src1 src2 ...)
#    This macro does the same as ADD_LIBRARY, but additionally
#    adds automoc4 handling for all source files.

# Internal helper macro, may change or be removed anytime:
# _ADD_AUTOMOC4_TARGET(<target_NAME> <SRCS_VAR>)
#
# Since version 0.9.88:
# The following two macros are only to be used for KDE4 projects
# and do something which makes sure automoc4 works for KDE. Don't
# use them anywhere else. See kdelibs/cmake/modules/KDE4Macros.cmake.
# _AUTOMOC4_KDE4_PRE_TARGET_HANDLING(<target_NAME> <SRCS_VAR>)
# _AUTOMOC4_KDE4_POST_TARGET_HANDLING(<target_NAME>)

#     Copyright (C) 2007 Matthias Kretz <kretz@kde.org>
#     Copyright (C) 2008-2009 Alexander Neundorf <neundorf@kde.org>
# 
#     Redistribution and use in source and binary forms, with or without
#     modification, are permitted provided that the following conditions
#     are met:
# 
#     1. Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#     2. Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
# 
#     THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
#     IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
#     OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
#     IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
#     INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
#     NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#     DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#     THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#     (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
#     THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# push the current cmake policy settings on the policy stack and pop them again at the
# end of this file, so any policies which are changed in this file don't affect anything
# on the outside (cmake_minimum_required() sets all policies to NEW for version 2.6.4). Alex
if(COMMAND cmake_policy)
  cmake_policy(PUSH)
endif(COMMAND cmake_policy)

# 2.6.4 is required because of the get_filename_component(REALPATH)
cmake_minimum_required( VERSION 2.6.4 FATAL_ERROR )

# allow duplicate target names, this is also done in FindKDE4Internal.cmake
cmake_policy(SET CMP0002 OLD)

get_filename_component(_AUTOMOC4_CURRENT_DIR  "${CMAKE_CURRENT_LIST_FILE}" PATH)

# set the automoc version number
include(${_AUTOMOC4_CURRENT_DIR}/Automoc4Version.cmake)

# are we in the source tree or already installed ?
if(EXISTS ${_AUTOMOC4_CURRENT_DIR}/kde4automoc.cpp)
   get_target_property(AUTOMOC4_EXECUTABLE automoc4 LOCATION)
   # this dependency is required to make parallel builds of kdesupport work:
   set(_AUTOMOC4_EXECUTABLE_DEP automoc4)
else(EXISTS ${_AUTOMOC4_CURRENT_DIR}/kde4automoc.cpp)
   get_filename_component(_AUTOMOC4_BIN_DIR  "${_AUTOMOC4_CURRENT_DIR}" PATH)
   get_filename_component(_AUTOMOC4_BIN_DIR  "${_AUTOMOC4_BIN_DIR}" PATH)

   # This REALPATH here is necessary for the case that the path is a "virtual" drive 
   # created using "subst", in this case otherwise the drive letter is missing:
   if(WIN32)
      get_filename_component(_AUTOMOC4_BIN_DIR  "${_AUTOMOC4_BIN_DIR}" REALPATH)
   endif(WIN32)
   find_program(AUTOMOC4_EXECUTABLE automoc4 PATHS  "${_AUTOMOC4_BIN_DIR}/bin" NO_DEFAULT_PATH)
   set(_AUTOMOC4_EXECUTABLE_DEP)
   mark_as_advanced(AUTOMOC4_EXECUTABLE)
endif(EXISTS ${_AUTOMOC4_CURRENT_DIR}/kde4automoc.cpp)


macro (AUTOMOC4_MOC_HEADERS _target_NAME)
   set (_headers_to_moc)
   foreach (_current_FILE ${ARGN})
      get_filename_component(_suffix "${_current_FILE}" EXT)
      if (".h" STREQUAL "${_suffix}" OR ".hpp" STREQUAL "${_suffix}" OR ".hxx" STREQUAL "${_suffix}" OR ".H" STREQUAL "${_suffix}")
         list(APPEND _headers_to_moc ${_current_FILE})
      else (".h" STREQUAL "${_suffix}" OR ".hpp" STREQUAL "${_suffix}" OR ".hxx" STREQUAL "${_suffix}" OR ".H" STREQUAL "${_suffix}")
         message(STATUS "AUTOMOC4_MOC_HEADERS: ignoring non-header file ${_current_FILE}")
      endif (".h" STREQUAL "${_suffix}" OR ".hpp" STREQUAL "${_suffix}" OR ".hxx" STREQUAL "${_suffix}" OR ".H" STREQUAL "${_suffix}")
   endforeach (_current_FILE)
   # need to create moc_<filename>.cpp file using automoc4
   # and add it to the target
   if(_headers_to_moc)
       set(_automoc4_headers_${_target_NAME} "${_headers_to_moc}")
       set(_automoc4_headers_${_target_NAME}_automoc "${_headers_to_moc}")
   endif(_headers_to_moc)
endmacro (AUTOMOC4_MOC_HEADERS)


macro(AUTOMOC4 _target_NAME _SRCS)
   set(_moc_files)

   # first list all explicitly set headers
   foreach(_header_to_moc ${_automoc4_headers_${_target_NAME}} )
      get_filename_component(_abs_header ${_header_to_moc} ABSOLUTE)
      list(APPEND _moc_files ${_abs_header})
   endforeach(_header_to_moc)

   # now add all the sources for the automoc
   foreach (_current_FILE ${${_SRCS}})
      get_filename_component(_abs_current_FILE "${_current_FILE}" ABSOLUTE)
      get_source_file_property(_skip      "${_abs_current_FILE}" SKIP_AUTOMOC)
      get_source_file_property(_generated "${_abs_current_FILE}" GENERATED)

      if(NOT  _generated  AND NOT  _skip)
         get_filename_component(_suffix "${_current_FILE}" EXT)
         # skip every source file that's not C++
         if(_suffix STREQUAL ".cpp" OR _suffix STREQUAL ".cc" OR _suffix STREQUAL ".cxx" OR _suffix STREQUAL ".C" OR _suffix STREQUAL ".mm")
             list(APPEND _moc_files ${_abs_current_FILE})
         endif(_suffix STREQUAL ".cpp" OR _suffix STREQUAL ".cc" OR _suffix STREQUAL ".cxx" OR _suffix STREQUAL ".C" OR _suffix STREQUAL ".mm")
      endif(NOT  _generated  AND NOT  _skip)
   endforeach (_current_FILE)

   if(_moc_files)
      set(_automoc_source "${CMAKE_CURRENT_BINARY_DIR}/${_target_NAME}_automoc.cpp")
      get_directory_property(_moc_incs INCLUDE_DIRECTORIES)
      get_directory_property(_moc_defs DEFINITIONS)
      get_directory_property(_moc_cdefs COMPILE_DEFINITIONS)

      # configure_file replaces _moc_files, _moc_incs, _moc_cdefs and _moc_defs
      configure_file(${_AUTOMOC4_CURRENT_DIR}/automoc4.files.in ${_automoc_source}.files)

      add_custom_command(OUTPUT ${_automoc_source}
         COMMAND ${AUTOMOC4_EXECUTABLE}
         ${_automoc_source}
         ${CMAKE_CURRENT_SOURCE_DIR}
         ${CMAKE_CURRENT_BINARY_DIR}
         ${QT_MOC_EXECUTABLE}
         ${CMAKE_COMMAND}
         --touch
         DEPENDS ${_automoc_source}.files ${_AUTOMOC4_EXECUTABLE_DEP}
         COMMENT ""
         VERBATIM
         )
      set(${_SRCS} ${_automoc_source} ${${_SRCS}})
   endif(_moc_files)
endmacro(AUTOMOC4)


macro(_ADD_AUTOMOC4_TARGET _target_NAME _SRCS)
   set(_moc_files)
   set(_moc_headers)

   # first list all explicitly set headers
   foreach(_header_to_moc ${_automoc4_headers_${_target_NAME}} )
      get_filename_component(_abs_header ${_header_to_moc} ABSOLUTE)
      list(APPEND _moc_files ${_abs_header})
      list(APPEND _moc_headers ${_abs_header})
   endforeach(_header_to_moc)

   # now add all the sources for the automoc
   foreach (_current_FILE ${${_SRCS}})
      get_filename_component(_abs_current_FILE "${_current_FILE}" ABSOLUTE)
      get_source_file_property(_skip      "${_abs_current_FILE}" SKIP_AUTOMOC)
      get_source_file_property(_generated "${_abs_current_FILE}" GENERATED)

      if(NOT  _generated  AND NOT  _skip)
         get_filename_component(_suffix "${_current_FILE}" EXT)
         # skip every source file that's not C++
         if(_suffix STREQUAL ".cpp" OR _suffix STREQUAL ".cc" OR _suffix STREQUAL ".cxx" OR _suffix STREQUAL ".C" OR _suffix STREQUAL ".mm")
             get_filename_component(_basename "${_current_FILE}" NAME_WE)
             get_filename_component(_abs_path "${_abs_current_FILE}" PATH)
             set(_header "${_abs_path}/${_basename}.h")
             if(EXISTS "${_header}")
                list(APPEND _moc_headers ${_header})
             endif(EXISTS "${_header}")
             set(_pheader "${_abs_path}/${_basename}_p.h")
             if(EXISTS "${_pheader}")
                list(APPEND _moc_headers ${_pheader})
             endif(EXISTS "${_pheader}")
             list(APPEND _moc_files ${_abs_current_FILE})
         endif(_suffix STREQUAL ".cpp" OR _suffix STREQUAL ".cc" OR _suffix STREQUAL ".cxx" OR _suffix STREQUAL ".C" OR _suffix STREQUAL ".mm")
      endif(NOT  _generated  AND NOT  _skip)
   endforeach (_current_FILE)

   if(_moc_files)
      set(_automoc_source "${CMAKE_CURRENT_BINARY_DIR}/${_target_NAME}.cpp")
      set(_automoc_dotFiles "${CMAKE_CURRENT_BINARY_DIR}/${_target_NAME}.cpp.files")
      get_directory_property(_moc_incs INCLUDE_DIRECTORIES)
      get_directory_property(_moc_defs DEFINITIONS)
      get_directory_property(_moc_cdefs COMPILE_DEFINITIONS)

      # configure_file replaces _moc_files, _moc_incs, _moc_cdefs and _moc_defs
      configure_file(${_AUTOMOC4_CURRENT_DIR}/automoc4.files.in ${_automoc_dotFiles})

      add_custom_target(${_target_NAME}
         COMMAND ${AUTOMOC4_EXECUTABLE}
         ${_automoc_source}
         ${CMAKE_CURRENT_SOURCE_DIR}
         ${CMAKE_CURRENT_BINARY_DIR}
         ${QT_MOC_EXECUTABLE}
         ${CMAKE_COMMAND}
         COMMENT ""
         VERBATIM
         )

      if(_AUTOMOC4_EXECUTABLE_DEP)
         add_dependencies(${_target_NAME} ${_AUTOMOC4_EXECUTABLE_DEP})
      endif(_AUTOMOC4_EXECUTABLE_DEP)

      set_source_files_properties(${_automoc_source} PROPERTIES GENERATED TRUE)
      get_directory_property(_extra_clean_files ADDITIONAL_MAKE_CLEAN_FILES)
      list(APPEND _extra_clean_files "${_automoc_source}")
      set_directory_properties(PROPERTIES ADDITIONAL_MAKE_CLEAN_FILES "${_extra_clean_files}")
      set(${_SRCS} ${_automoc_source} ${${_SRCS}})
   endif(_moc_files)
endmacro(_ADD_AUTOMOC4_TARGET)


macro(AUTOMOC4_ADD_EXECUTABLE _target_NAME)
   set(_SRCS ${ARGN})

   set(_add_executable_param)
   foreach(_argName "WIN32" "MACOSX_BUNDLE" "EXCLUDE_FROM_ALL")
      list(FIND _SRCS ${_argName} _index)
      if(_index GREATER -1)
         list(APPEND _add_executable_param ${_argName})
         list(REMOVE_AT _SRCS ${_index})
      endif(_index GREATER -1)
   endforeach(_argName)

   _add_automoc4_target("${_target_NAME}_automoc" _SRCS)
   add_executable(${_target_NAME} ${_add_executable_param} ${_SRCS})
   add_dependencies(${_target_NAME} "${_target_NAME}_automoc")

endmacro(AUTOMOC4_ADD_EXECUTABLE)


macro(AUTOMOC4_ADD_LIBRARY _target_NAME)
   set(_SRCS ${ARGN})

   set(_add_executable_param)
   foreach(_argName "STATIC" "SHARED" "MODULE" "EXCLUDE_FROM_ALL")
      list(FIND _SRCS ${_argName} _index)
      if(_index GREATER -1)
         list(APPEND _add_executable_param ${_argName})
         list(REMOVE_AT _SRCS ${_index})
      endif(_index GREATER -1)
   endforeach(_argName)

   _add_automoc4_target("${_target_NAME}_automoc" _SRCS)
   add_library(${_target_NAME} ${_add_executable_param} ${_SRCS})
   add_dependencies(${_target_NAME} "${_target_NAME}_automoc")
endmacro(AUTOMOC4_ADD_LIBRARY)


macro(_AUTOMOC4_KDE4_PRE_TARGET_HANDLING _target _srcs)
   _add_automoc4_target("${_target}_automoc" ${_srcs})
endmacro(_AUTOMOC4_KDE4_PRE_TARGET_HANDLING)


macro(_AUTOMOC4_KDE4_POST_TARGET_HANDLING _target)
   add_dependencies(${_target} "${_target}_automoc")
endmacro(_AUTOMOC4_KDE4_POST_TARGET_HANDLING)


# restore previous policy settings:
if(COMMAND cmake_policy)
  cmake_policy(POP)
endif(COMMAND cmake_policy)
