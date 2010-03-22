project(ZLIB)
cmake_minimum_required(VERSION 2.6)

set(zlib_SRCS
    adler32.c
    compress.c
    crc32.c
    deflate.c
    gzclose.c
    gzlib.c
    gzread.c
    gzwrite.c
    infback.c
    inffast.c
    inflate.c
    inftrees.c
    minigzip.c
    trees.c
    uncompr.c
    zutil.c
)
set(zlib_HDRS
    crc32.h
    deflate.h
    gzguts.h
    inffast.h
    inffixed.h
    inflate.h
    inftrees.h
    trees.h
    zutil.h
)
set(zlib_HDRS_install
    zconf.h
    zlib.h
)
if(WIN32)
    LIST(APPEND zlib_SRCS win32/zlib.def)
endif(WIN32)
if(MSVC)
    ADD_DEFINITIONS(-D_CRT_SECURE_NO_DEPRECATE -D_CRT_NONSTDC_NO_DEPRECATE)
    SET(CMAKE_C_FLAGS_RELEASE             "${CMAKE_C_FLAGS_RELEASE} /GL")
    SET(CMAKE_CXX_FLAGS_RELEASE           "${CMAKE_CXX_FLAGS_RELEASE} /GL")
    SET(CMAKE_EXE_LINKER_FLAGS_RELEASE    "${CMAKE_EXE_LINKER_FLAGS_RELEASE} /LTCG")
    SET(CMAKE_MODULE_LINKER_FLAGS_RELEASE "${CMAKE_MODULE_LINKER_FLAGS_RELEASE} /LTCG")
    SET(CMAKE_SHARED_LINKER_FLAGS_RELEASE "${CMAKE_SHARED_LINKER_FLAGS_RELEASE} /LTCG")
endif(MSVC)

add_library(zlib SHARED ${zlib_SRCS} ${zlib_HDRS} ${zlib_HDRS_install})
install(TARGETS zlib RUNTIME DESTINATION bin
                     LIBRARY DESTINATION lib
                     ARCHIVE DESTINATION lib
)
install(FILES ${zlib_HDRS_install} DESTINATION include)
