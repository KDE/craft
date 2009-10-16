project(ofx)

set (VERSION_MAJOR 0)
set (VERSION_MINOR 9)
set (VERSION_PATH 1)

cmake_minimum_required(VERSION 2.6)

list(APPEND CMAKE_MODULE_PATH  ${CMAKE_SOURCE_DIR})
find_package(OpenSP REQUIRED)

include_directories(
    inc
    ${OPENSP_INCLUDES}
#   ${KDE4_INCLUDES}
    $ENV{KDEROOT}/include
)

add_definitions(
    -DOS_WIN32
)

set (COEFF_HDRS 
        inc/libofx.h
        lib/messages.hh
        lib/ofx_preproc.hh
        lib/file_preproc.hh
        lib/context.hh
        lib/ofx_sgml.hh
        lib/ofc_sgml.hh
        lib/ofx_aggregate.hh
        lib/ofx_error_msg.hh
        lib/ofx_containers.hh
        lib/ofx_request.hh
        lib/ofx_request_accountinfo.hh
        lib/ofx_request_statement.hh
        lib/ofx_utilities.hh
        lib/tree.hh
        lib/win32.hh
        )

set (SRC_SOURCES
         lib/messages.cpp
         lib/ofx_utilities.cpp
         lib/file_preproc.cpp
         lib/context.cpp
         lib/ofx_preproc.cpp
         lib/ofx_container_generic.cpp
         lib/ofx_container_main.cpp
         lib/ofx_container_security.cpp
         lib/ofx_container_statement.cpp
         lib/ofx_container_account.cpp
         lib/ofx_container_transaction.cpp
         lib/ofx_containers_misc.cpp
         lib/ofx_request.cpp
         lib/ofx_request_accountinfo.cpp
         lib/ofx_request_statement.cpp
         lib/ofx_sgml.cpp
         lib/ofc_sgml.cpp
         lib/win32.cpp
         ${COEFF_HDRS}
)

# We would like it to be shared, but libofx does not export symbols manually
# thus it causes troubles on MSVC
#add_library(ofx SHARED ${SRC_SOURCES})
add_library(ofx ${SRC_SOURCES})

set_target_properties(ofx PROPERTIES OUTPUT_NAME "libofx")
target_link_libraries(ofx ${OPENSP_LIBRARIES} $ENV{KDEROOT}/lib/libiconv-2.lib)

install(TARGETS ofx RUNTIME DESTINATION bin ARCHIVE DESTINATION lib LIBRARY DESTINATION lib)
install(FILES inc/libofx.h DESTINATION include/libofx)
