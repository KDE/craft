project(libdvdcss)

cmake_minimum_required(VERSION 2.6)

configure_file(${CMAKE_SOURCE_DIR}/config.h ${CMAKE_BINARY_DIR}/config.h)
file(APPEND ${CMAKE_BINARY_DIR}/config.h "#define MAX_PATH 260\n")

file(WRITE ${CMAKE_BINARY_DIR}/common.h "")
add_definitions(
	-DWIN32
	-DLIBDVDCSS_EXPORTS
)

include_directories(
	${CMAKE_BINARY_DIR}
)

set (libdvdcss_SOURCES
	src/libdvdcss.c 
	src/libdvdcss.h
	src/device.c 
	src/device.h
	src/css.c 
	src/css.h 
	src/csstables.h
	src/ioctl.c 
	src/ioctl.h
	src/error.c
	src/common.h
)

add_library(dvdcss SHARED ${libdvdcss_SOURCES})
target_link_libraries(dvdcss)

install(TARGETS dvdcss RUNTIME DESTINATION bin ARCHIVE DESTINATION lib LIBRARY DESTINATION lib)
install(FILES src/dvdcss/dvdcss.h DESTINATION include/dvdcss)
