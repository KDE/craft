project(bzip2)
cmake_minimum_required(VERSION 2.6)

set(bzip2_lib_SRCS
    blocksort.c
    huffman.c
    crctable.c
    randtable.c
    compress.c
    decompress.c
    bzlib.c
)

set(bzip2_scripts
    bzdiff
    bzgrep
    bzmore
)
set(bzip2_docs
    bzip2.txt
    manual.pdf
)
set(bzip2_html
    manual.html
)

set(CMAKE_DEBUG_POSTFIX "d")
if(MSVC)
  add_definitions(-D_CRT_SECURE_NO_DEPRECATE -D_CRT_NONSTDC_NO_DEPRECATE)
  set(CMAKE_C_FLAGS_RELEASE             "${CMAKE_C_FLAGS_RELEASE} /GL")
  set(CMAKE_CXX_FLAGS_RELEASE           "${CMAKE_CXX_FLAGS_RELEASE} /GL")
  set(CMAKE_EXE_LINKER_FLAGS_RELEASE    "${CMAKE_EXE_LINKER_FLAGS_RELEASE} /LTCG")
  set(CMAKE_MODULE_LINKER_FLAGS_RELEASE "${CMAKE_MODULE_LINKER_FLAGS_RELEASE} /LTCG")
  set(CMAKE_SHARED_LINKER_FLAGS_RELEASE "${CMAKE_SHARED_LINKER_FLAGS_RELEASE} /LTCG")
endif(MSVC)

add_library(bzip2 SHARED ${bzip2_lib_SRCS})
if(WIN32)
  set_target_properties(bzip2 PROPERTIES PREFIX "")
endif(WIN32)

# bzip2recover
add_executable(bzip2recover bzip2recover.c)
target_link_libraries(bzip2recover bzip2)
# bzip2
add_executable(bzip2_bin bzip2.c)
target_link_libraries(bzip2_bin bzip2)
set_target_properties(bzip2_bin PROPERTIES OUTPUT_NAME bzip2)

file(GLOB man1 ${bzip2_SOURCE_DIR}/*.1)

install_targets(/lib bzip2)
install_targets(/bin bzip2recover)
install_targets(/bin bzip2_bin)
if(NOT WIN32)
  install(PROGRAMS ${bzip2_scripts} DESTINATION bin)
endif(NOT WIN32)
install(FILES ${man1}          DESTINATION man/man1)
install(FILES ${bzip2_docs}    DESTINATION doc)
install(FILES ${bzip2_html}    DESTINATION doc/html)
install(FILES bzlib.h          DESTINATION include)

# echo EXPORTS > bzip2.def
# nm bzip2.dll | grep ' T _' | sed 's/.* T _//' >> bzip2.def
# pexports bzip2.dll > bzip2.def
# lib /def:bzip2.def /machine:x86
