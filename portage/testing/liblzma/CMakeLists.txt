project(liblzma)
include(CheckIncludeFiles)
include(CheckFunctionExists)
include(CheckSymbolExists)
include(CheckTypeSize)

include_directories(${CMAKE_CURRENT_BINARY_DIR} src/common src/liblzma/api src/liblzma/common src/liblzma/check src/liblzma/rangecoder src/liblzma/lz src/liblzma/lzma src/liblzma/delta src/liblzma/simple src/liblzma/subblock)

check_include_files(biteswap.h HAVE_BYTESWAP_H)
check_include_files(dlfcn.h HAVE_DLFCN_H)
check_include_files(fcntl.h HAVE_FCNTL_H)
check_include_files(getopt.h HAVE_GETOPT_H)
check_include_files(inttypes.h HAVE_INTTYPES_H)
check_include_files(limits.h HAVE_LIMITS_H)
check_include_files(memory.h HAVE_MEMORY_H)
check_include_files(stdbool.h HAVE_STDBOOL_H)
check_include_files(stdint.h HAVE_STDINT_H)
check_include_files(stdlib.h HAVE_STDLIB_H)
check_include_files(strings.h HAVE_STRINGS_H)
check_include_files(string.h HAVE_STRING_H)
check_include_files(sys/param.h HAVE_SYS_PARAM_H)
check_include_files(sys/stat.h HAVE_SYS_STAT_H)
check_include_files(sys/sysctl.h HAVE_SYS_SYSCTL_H)
check_include_files(sys/time.h HAVE_SYS_TIME_H)
check_include_files(sys/types.h HAVE_SYS_TYPES_H)
check_include_files(unistd.h HAVE_UNISTD_H)
check_include_files(pthread.h HAVE_PTHREAD)

set(HAVE_ASM_X86 1)
set(HAVE_CHECK_CRC64 1)
set(HAVE_CHECK_SHA256 1)
set(HAVE_DECODER 1)
set(HAVE_DECODER_ARM 1)
set(HAVE_DECODER_ARMTHUMB 1)
set(HAVE_DECODER_DELTA 1)
set(HAVE_DECODER_IA64 1)
set(HAVE_DECODER_LZMA1 1)
set(HAVE_DECODER_LZMA2 1)
set(HAVE_DECODER_POWERPC 1)
set(HAVE_DECODER_SPARC 1)
set(HAVE_DECODER_SUBBLOCK 0)
set(HAVE_DECODER_X86 1)
set(HAVE_ENCODER 1)
set(HAVE_ENCODER_ARM 1)
set(HAVE_ENCODER_ARMTHUMB 1)
set(HAVE_ENCODER_DELTA 1)
set(HAVE_ENCODER_IA64 1)
set(HAVE_ENCODER_LZMA1 1)
set(HAVE_ENCODER_LZMA2 1)
set(HAVE_ENCODER_POWERPC 1)
set(HAVE_ENCODER_SPARC 1)
set(HAVE_ENCODER_SUBBLOCK 0)
set(HAVE_ENCODER_X86 1)
set(HAVE_FAST_UNALIGNED_ACCESS 1)
set(HAVE_MF_BT2 1)
set(HAVE_MF_BT3 1)
set(HAVE_MF_BT4 1)
set(HAVE_MF_HC3 1)
set(HAVE_MF_HC4 1)
set(HAVE_MF_BT3 1)
set(STDC_HEADERS 1)

check_function_exists(bswap_16 HAVE_BSWAP_16)
check_function_exists(bswap_32 HAVE_BSWAP_32)
check_function_exists(bswap_64 HAVE_BSWAP_64)
check_function_exists(dcgettext HAVE_DCGETTEXT)
check_function_exists(futimens HAVE_FUTIMENS)
check_function_exists(futimes HAVE_FUTIMES)
check_function_exists(futimesat HAVE_FUTIMESAT)
check_function_exists(gettext HAVE_GETTEXT)
check_function_exists(iconv HAVE_ICONV)
check_function_exists(utime HAVE_UTIME)
check_function_exists(utimes HAVE_UTIMES)

check_symbol_exists(OPTRESET "getopt.h" HAVE_OPTRESET)

set(CMAKE_EXTRA_INCLUDE_FILES "stdint.h")

check_type_size(size_t SIZEOF_SIZE_T)
check_type_size(uintptr_t UINTPTR_T)
check_type_size(int8_t      INT8_T)
check_type_size(uint8_t     UINT8_T)
check_type_size(int16_t     INT16_T)
check_type_size(uint16_t    UINT16_T)
check_type_size(int32_t     INT32_T)
check_type_size(uint32_t    UINT32_T)
check_type_size(int64_t     INT64_T)
check_type_size(uint64_t    UINT64_T)

SET(CMAKE_EXTRA_INCLUDE_FILES)


configure_file(config.h.cmake config.h)

set(LZMA_SRC src/liblzma/common/alone_decoder.c
    src/liblzma/common/alone_encoder.c
    src/liblzma/common/auto_decoder.c
    src/liblzma/common/block_buffer_decoder.c
    src/liblzma/common/block_buffer_encoder.c
    src/liblzma/common/block_decoder.c
    src/liblzma/common/block_encoder.c
    src/liblzma/common/block_header_decoder.c
    src/liblzma/common/block_header_encoder.c
    src/liblzma/common/block_util.c
    src/liblzma/common/common.c
    src/liblzma/common/easy_buffer_encoder.c
    src/liblzma/common/easy_decoder_memusage.c
    src/liblzma/common/easy_encoder.c
    src/liblzma/common/easy_encoder_memusage.c
    src/liblzma/common/easy_preset.c
    src/liblzma/common/filter_common.c
    src/liblzma/common/filter_decoder.c
    src/liblzma/common/filter_encoder.c
    src/liblzma/common/filter_flags_decoder.c
    src/liblzma/common/filter_flags_encoder.c
    src/liblzma/common/index.c
    src/liblzma/common/index_decoder.c
    src/liblzma/common/index_encoder.c
    src/liblzma/common/index_hash.c
    src/liblzma/common/stream_buffer_decoder.c
    src/liblzma/common/stream_buffer_encoder.c
    src/liblzma/common/stream_decoder.c
    src/liblzma/common/stream_encoder.c
    src/liblzma/common/stream_flags_common.c
    src/liblzma/common/stream_flags_decoder.c
    src/liblzma/common/stream_flags_encoder.c
    src/liblzma/common/vli_decoder.c
    src/liblzma/common/vli_encoder.c
    src/liblzma/common/vli_size.c
    src/liblzma/check/check.c
    src/liblzma/check/crc32_table.c
    src/liblzma/check/crc64_table.c
    src/liblzma/check/sha256.c
    src/liblzma/rangecoder/price_table.c
    src/liblzma/lz/lz_decoder.c
    src/liblzma/lz/lz_encoder.c
    src/liblzma/lz/lz_encoder_mf.c
    src/liblzma/lzma/fastpos_table.c
    src/liblzma/lzma/fastpos_tablegen.c
    src/liblzma/lzma/lzma2_decoder.c
    src/liblzma/lzma/lzma2_encoder.c
    src/liblzma/lzma/lzma_decoder.c
    src/liblzma/lzma/lzma_encoder.c
    src/liblzma/lzma/lzma_encoder_optimum_fast.c
    src/liblzma/lzma/lzma_encoder_optimum_normal.c
    src/liblzma/lzma/lzma_encoder_presets.c
    src/liblzma/delta/delta_common.c
    src/liblzma/delta/delta_decoder.c
    src/liblzma/delta/delta_encoder.c
    src/liblzma/simple/arm.c
    src/liblzma/simple/armthumb.c
    src/liblzma/simple/ia64.c
    src/liblzma/simple/powerpc.c
    src/liblzma/simple/simple_coder.c
    src/liblzma/simple/simple_decoder.c
    src/liblzma/simple/simple_encoder.c
    src/liblzma/simple/sparc.c
    src/liblzma/simple/x86.c

    src/liblzma/check/crc32_fast.c
    src/liblzma/check/crc64_fast.c
#     src/liblzma/check/crc32_x86.S
#     src/liblzma/check/crc64_x86.S
    )

set(CMAKE_C_FLAGS ${CMAKE_CXX_FLAGS} "-DHAVE_CONFIG_H -std=gnu99 -mms-bitfields")

add_library(lzma SHARED ${LZMA_SRC})
install(TARGETS lzma RUNTIME DESTINATION bin ARCHIVE DESTINATION lib)

set(XDEC_SRC src/xzdec/xzdec.c)
add_executable(xzdec ${XDEC_SRC})
target_link_libraries(xzdec lzma)
install(TARGETS xzdec RUNTIME DESTINATION bin ARCHIVE DESTINATION lib)

add_executable(lzmadec ${XDEC_SRC})
set_property(TARGET lzmadec PROPERTY COMPILE_DEFINITIONS LZMADEC)
target_link_libraries(lzmadec lzma)
install(TARGETS lzmadec RUNTIME DESTINATION bin ARCHIVE DESTINATION lib)

set(XZ_SRC  src/xz/args.c
    src/xz/hardware.c
    src/xz/coder.c
    src/xz/coder.h
    src/xz/file_io.c
    src/xz/main.c
    src/xz/message.c
    src/xz/options.c
    src/xz/signals.c
    src/xz/suffix.c
    src/xz/util.c)

add_executable(xz ${XZ_SRC})
target_link_libraries(xz lzma)

if(HAVE_PTHREAD)
    target_link_libraries(xz pthread)
endif(HAVE_PTHREAD)

install(TARGETS xz RUNTIME DESTINATION bin ARCHIVE DESTINATION lib)

install(DIRECTORY src/liblzma/api/ DESTINATION include FILES_MATCHING PATTERN "*.h")


set(LZMAINFO_SRC src/lzmainfo/lzmainfo.c)
add_executable(lzmainfo ${LZMAINFO_SRC})
target_link_libraries(lzmainfo lzma)
install(TARGETS lzmainfo RUNTIME DESTINATION bin ARCHIVE DESTINATION lib)
