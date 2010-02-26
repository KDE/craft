PROJECT(zlib)
CMAKE_MINIMUM_REQUIRED(VERSION 2.8)

SET(zlib_SRCS
    adler32.c
    compress.c
    crc32.c
    deflate.c
    gzio.c
    infback.c
    inffast.c
    inflate.c
    inftrees.c
    minigzip.c
    trees.c
    uncompr.c
    zutil.c
)
SET(zlib_HDRS
    crc32.h
    deflate.h
    inffast.h
    inffixed.h
    inflate.h
    inftrees.h
    trees.h
    zutil.h
)
SET(zlib_HDRS_install
    zconf.h
    zlib.h
)
IF(WIN32)
    LIST(APPEND zlib_SRCS win32/zlib.def)
ENDIF(WIN32)
IF(MSVC)
    ADD_DEFINITIONS(-D_CRT_SECURE_NO_DEPRECATE -D_CRT_NONSTDC_NO_DEPRECATE)
    SET(CMAKE_C_FLAGS_RELEASE             "${CMAKE_C_FLAGS_RELEASE} /GL")
    SET(CMAKE_CXX_FLAGS_RELEASE           "${CMAKE_CXX_FLAGS_RELEASE} /GL")
    SET(CMAKE_EXE_LINKER_FLAGS_RELEASE    "${CMAKE_EXE_LINKER_FLAGS_RELEASE} /LTCG")
    SET(CMAKE_MODULE_LINKER_FLAGS_RELEASE "${CMAKE_MODULE_LINKER_FLAGS_RELEASE} /LTCG")
    SET(CMAKE_SHARED_LINKER_FLAGS_RELEASE "${CMAKE_SHARED_LINKER_FLAGS_RELEASE} /LTCG")
ENDIF(MSVC)

ADD_LIBRARY(zlib SHARED ${zlib_SRCS} ${zlib_HDRS} ${zlib_HDRS_install})
INSTALL(TARGETS zlib RUNTIME DESTINATION bin
                     LIBRARY DESTINATION lib
                     ARCHIVE DESTINATION lib
)
INSTALL(FILES ${zlib_HDRS_install} DESTINATION include)
