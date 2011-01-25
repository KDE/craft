cmake_minimum_required(VERSION 2.8)
project(glee)

set(glee_SRCS
    ${CMAKE_SOURCE_DIR}/glee.c
)

set(glee_HDRS
    ${CMAKE_SOURCE_DIR}/glee.h
)

add_library(glee ${glee_SRCS})

install(TARGETS glee
                RUNTIME DESTINATION bin
                LIBRARY DESTINATION lib
                ARCHIVE DESTINATION lib
)

install(FILES ${glee_HDRS} DESTINATION include/GL)
