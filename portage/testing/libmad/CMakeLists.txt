project(libmad)

cmake_minimum_required(VERSION 2.6)

list(APPEND CMAKE_MODULE_PATH  ${CMAKE_SOURCE_DIR})
find_package(kdewin32 REQUIRED)

option(ENABLE_ASO "architecture-specific optimizations" on) 
if (ENABLE_ASO)
    add_definitions(
        -DASO_ZEROCHECK
)
endif (ENABLE_ASO)

option(ENABLE_DEBUG, "enable diagnostic debugging support" off)
if (ENABLE_DEBUG)
    add_definitions(
        -DDEBUG
    )        
endif (ENABLE_DEBUG)

add_definitions(
	-DWIN32
    -DFPM_INTEL
)

if (MSVC)
    add_definitions(
        -Dinline=__inline
    )
endif (MSVC)

include_directories(
	${CMAKE_BINARY_DIR}/msvc++
	${KDEWIN32_INCLUDES}
)

set (exported_headers 
    version.h 
    fixed.h 
    bit.h 
    timer.h 
    stream.h 
    frame.h 
    synth.h 
    decoder.h
)

set (headers 
    ${exported_headers}
    global.h 
    layer12.h 
    layer3.h 
    huffman.h
)

set (data_includes 
    D.dat 
    imdct_s.dat 
    qc_table.dat 
    rq_table.dat
    sf_table.dat
)  

set (libmad_SOURCES
    version.c 
    fixed.c 
    bit.c 
    timer.c 
    stream.c 
    frame.c
    synth.c 
    decoder.c 
    layer12.c 
    layer3.c 
    huffman.c  
    ${headers}
)

add_library(mad ${libmad_SOURCES})
target_link_libraries(mad)

install(TARGETS mad RUNTIME DESTINATION bin ARCHIVE DESTINATION lib LIBRARY DESTINATION lib)
if (MSVC)
    install(FILES msvc++/mad.h DESTINATION include)
else (MSVC)
    install(FILES ${CMAKE_BINARY_DIR}/mad.h DESTINATION include)
endif (MSVC)

add_executable(minimad minimad.c)
target_link_libraries(minimad mad ${KDEWIN32_LIBRARIES})
