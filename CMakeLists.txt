project(emerge LANGUAGES NONE)
cmake_minimum_required(VERSION 2.8.12)

enable_testing()

add_test(NAME emergetests
   COMMAND ${CMAKE_CURRENT_BINARY_DIR}/bin/test/runtests.py -v
   WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/bin/test)
