# ########## Project setup ##########
PROJECT(gmp-4.1)
CMAKE_MINIMUM_REQUIRED(VERSION 2.4.5)

# ######### General setup ##########
INCLUDE_DIRECTORIES(${CMAKE_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR})
INCLUDE (CheckIncludeFiles)
INCLUDE (CheckFunctionExists)

# ########## gmp-4.1 executable ##########
# Sources:
SET(gmp-4.1_executable_SRCS
    ansi2knr.c
#    tal-debug.c
#    tal-notreent.c
#    tal-reent.c
    assert.c
    compat.c
    errno.c
    extract-dbl.c
    insert-dbl.c
    memory.c
    mp_bpl.c
    mp_clz_tab.c
    mp_minv_tab.c
    mp_set_fns.c
    rand.c
    rands.c
    randclr.c
    randdef.c
    randlc.c
    randlc2s.c
    randlc2x.c
    randraw.c
    randsd.c
    randsdui.c
    version.c
    dummy.cc
)

# Headers:
SET(gmp-4.1_executable_HDRS
    acconfig.h
    install-sh
    ltmain.sh
    mdate-sh
    gmp-impl.h
    longlong.h
    gmpxx.h
    mpfrxx.h
)

SET(HAVE_HOST_CPU_FAMILY_powerpc 0)
SET(HAVE_HOST_CPU_FAMILY_power 0)
SET(GMP_NAIL_BITS 0 CACHE STRING "")

IF (CMAKE_SIZEOF_VOID_P MATCHES "8")
    SET(BITS_PER_MP_LIMB 64)
ELSE(CMAKE_SIZEOF_VOID_P MATCHES "8")
    SET(BITS_PER_MP_LIMB 32)    
ENDIF(CMAKE_SIZEOF_VOID_P MATCHES "8")

#not sure if this is right
SET(DEFN_LONG_LONG_LIMB "/* #undef _LONG_LONG_LIMB */")

SET(LIBGMP_DLL 1)
#SET(WANT_TMP_DEBUG 1)
SET(WANT_TMP_ALLOCA 1)
SET(WANT_FFT 1)
SET(STDC_HEADERS 1)

CHECK_FUNCTION_EXISTS(vsnprintf HAVE_VSNPRINTF)
CHECK_FUNCTION_EXISTS(times HAVE_TIMES)

CHECK_INCLUDE_FILES(unistd.h HAVE_UNISTD_H)
CHECK_INCLUDE_FILES(sys/types.h HAVE_SYS_TYPES_H)
CHECK_INCLUDE_FILES(sys/time.h HAVE_SYS_TIME_H)
CHECK_INCLUDE_FILES(sys/times.h HAVE_SYS_TIMES_H)
CHECK_INCLUDE_FILES(sys/systemcfg.h HAVE_SYS_SYSTEMCFG_H)
CHECK_INCLUDE_FILES(sys/syssgi.h HAVE_SYS_SYSSGI_H)
CHECK_INCLUDE_FILES(sys/sysctl.h HAVE_SYS_SYSCTL_H)
CHECK_INCLUDE_FILES(sys/stat.h HAVE_SYS_STAT_H)
CHECK_INCLUDE_FILES(sys/resource.h HAVE_SYS_RESOURCE_H)
CHECK_INCLUDE_FILES(sys/processor.h HAVE_SYS_PROCESSOR_H)
CHECK_INCLUDE_FILES(sys/param.h HAVE_SYS_PARAM_H)
CHECK_INCLUDE_FILES(sys/mman.h HAVE_SYS_MMAN_H)
CHECK_INCLUDE_FILES(stdarg.h HAVE_STDARG)

#we should choose the right gmp-mparam by the type of processor but I don't know how to do that
CONFIGURE_FILE(mpn/x86/i486/gmp-mparam.h ${CMAKE_BINARY_DIR}/gmp-mparam.h COPYONLY)
CONFIGURE_FILE(stamp-h1.in ${CMAKE_BINARY_DIR}/stamp.h1)
#CONFIGURE_FILE(Makefile.in ${CMAKE_BINARY_DIR}/Makefile)
CONFIGURE_FILE(config.in ${CMAKE_BINARY_DIR}/config.h)
#CONFIGURE_FILE(configure.in ${CMAKE_BINARY_DIR}/configure)
CONFIGURE_FILE(gmp-h.in ${CMAKE_BINARY_DIR}/gmp.h)
CONFIGURE_FILE(mp-h.in ${CMAKE_BINARY_DIR}/mp.h)

SET(CMAKE_C_FLAGS "-DHAVE_CONFIG_H")

# actual target:
ADD_LIBRARY(gmp-4.1 ${gmp-4.1_executable_SRCS})

# add install target:
INSTALL(TARGETS gmp-4.1 DESTINATION bin)
