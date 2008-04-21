# ########## Project setup ##########
PROJECT(gmp-4.1)
CMAKE_MINIMUM_REQUIRED(VERSION 2.4.5)

# ######### General setup ##########
INCLUDE_DIRECTORIES(${CMAKE_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR})
INCLUDE (CheckIncludeFiles)
INCLUDE (CheckFunctionExists)
INCLUDE (CheckCSourceCompiles)
INCLUDE (CheckTypeSize)

# ########## gmp-4.1 executable ##########
# Sources:
SET(gmp-4.1_executable_SRCS
#     ansi2knr.c
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

SET(mpf_SRCS
   mpf/iset_ui.c
   mpf/abs.c
   mpf/add.c
   mpf/add_ui.c
   mpf/ceilfloor.c
   mpf/clear.c
   mpf/cmp.c
   mpf/cmp_d.c
   mpf/cmp_si.c
   mpf/cmp_ui.c
   mpf/div.c
   mpf/div_2exp.c
   mpf/div_ui.c
   mpf/dump.c
   mpf/eq.c
   mpf/fits_sint.c
   mpf/fits_slong.c
   mpf/fits_sshort.c
   mpf/fits_uint.c
   mpf/fits_ulong.c
   mpf/fits_ushort.c
   mpf/get_d.c
   mpf/get_dfl_prec.c
   mpf/get_d_2exp.c
   mpf/get_prc.c
   mpf/get_si.c
   mpf/get_str.c
   mpf/get_ui.c
   mpf/init.c
   mpf/init2.c
   mpf/inp_str.c
   mpf/int_p.c
   mpf/iset.c
   mpf/iset_d.c
   mpf/iset_si.c
   mpf/iset_str.c
   mpf/mul.c
   mpf/mul_2exp.c
   mpf/mul_ui.c
   mpf/neg.c
   mpf/out_str.c
   mpf/pow_ui.c
   mpf/random2.c
   mpf/reldiff.c
   mpf/set.c
   mpf/set_d.c
   mpf/set_dfl_prec.c
   mpf/set_prc.c
   mpf/set_prc_raw.c
   mpf/set_q.c
   mpf/set_si.c
   mpf/set_str.c
   mpf/set_ui.c
   mpf/set_z.c
   mpf/size.c
   mpf/sqrt.c
   mpf/sqrt_ui.c
   mpf/sub.c
   mpf/sub_ui.c
   mpf/swap.c
   mpf/trunc.c
   mpf/ui_div.c
   mpf/ui_sub.c
   mpf/urandomb.c
)

SET(mpz_SRCS
    mpz/add.c
    mpz/add_ui.c
    mpz/abs.c
    mpz/aorsmul.c
    mpz/aorsmul_i.c
    mpz/and.c
    mpz/array_init.c
    mpz/bin_ui.c
    mpz/bin_uiui.c
    mpz/cdiv_q.c
    mpz/cdiv_q_ui.c
    mpz/cdiv_qr.c
    mpz/cdiv_qr_ui.c
    mpz/cdiv_r.c
    mpz/cdiv_r_ui.c
    mpz/cdiv_ui.c
    mpz/cfdiv_q_2exp.c
    mpz/cfdiv_r_2exp.c
    mpz/clear.c
    mpz/clrbit.c
    mpz/cmp.c
    mpz/cmp_d.c
    mpz/cmp_si.c
    mpz/cmp_ui.c
    mpz/cmpabs.c
    mpz/cmpabs_d.c
    mpz/cmpabs_ui.c
    mpz/com.c
    mpz/cong.c
    mpz/cong_2exp.c
    mpz/cong_ui.c
    mpz/divexact.c
    mpz/divegcd.c
    mpz/dive_ui.c
    mpz/divis.c
    mpz/divis_ui.c
    mpz/divis_2exp.c
    mpz/dump.c
    mpz/export.c
    mpz/fac_ui.c
    mpz/fdiv_q.c
    mpz/fdiv_q_ui.c
    mpz/fdiv_qr.c
    mpz/fdiv_qr_ui.c
    mpz/fdiv_r.c
    mpz/fdiv_r_ui.c
    mpz/fdiv_ui.c
    mpz/fib_ui.c
    mpz/fib2_ui.c
    mpz/fits_sint.c
    mpz/fits_slong.c
    mpz/fits_sshort.c
    mpz/fits_uint.c
    mpz/fits_ulong.c
    mpz/fits_ushort.c
    mpz/gcd.c
    mpz/gcd_ui.c
    mpz/gcdext.c
    mpz/get_d.c
    mpz/get_d_2exp.c
    mpz/get_si.c
    mpz/get_str.c
    mpz/get_ui.c
    mpz/getlimbn.c
    mpz/hamdist.c
    mpz/import.c
    mpz/init.c
    mpz/init2.c
    mpz/inp_raw.c
    mpz/inp_str.c
    mpz/invert.c
    mpz/ior.c
    mpz/iset.c
    mpz/iset_d.c
    mpz/iset_si.c
    mpz/iset_str.c
    mpz/iset_ui.c
    mpz/jacobi.c
    mpz/kronsz.c
    mpz/kronuz.c
    mpz/kronzs.c
    mpz/kronzu.c
    mpz/lcm.c
    mpz/lcm_ui.c
    mpz/lucnum_ui.c
    mpz/lucnum2_ui.c
    mpz/millerrabin.c
    mpz/mod.c
    mpz/mul.c
    mpz/mul_2exp.c
    mpz/mul_si.c
    mpz/mul_ui.c
    mpz/n_pow_ui.c
    mpz/neg.c
    mpz/nextprime.c
    mpz/out_raw.c
    mpz/out_str.c
    mpz/perfpow.c
    mpz/perfsqr.c
    mpz/popcount.c
    mpz/pow_ui.c
    mpz/powm.c
    mpz/powm_ui.c
    mpz/pprime_p.c
    mpz/random.c
    mpz/random2.c
    mpz/realloc.c
    mpz/realloc2.c
    mpz/remove.c
    mpz/root.c
    mpz/rrandomb.c
    mpz/scan0.c
    mpz/scan1.c
    mpz/set.c
    mpz/set_d.c
    mpz/set_f.c
    mpz/set_q.c
    mpz/set_si.c
    mpz/set_str.c
    mpz/set_ui.c
    mpz/setbit.c
    mpz/size.c
    mpz/sizeinbase.c
    mpz/sqrt.c
    mpz/sqrtrem.c
    mpz/sub.c
    mpz/sub_ui.c
    mpz/swap.c
    mpz/tdiv_ui.c
    mpz/tdiv_q.c
    mpz/tdiv_q_2exp.c
    mpz/tdiv_q_ui.c
    mpz/tdiv_qr.c
    mpz/tdiv_qr_ui.c
    mpz/tdiv_r.c
    mpz/tdiv_r_2exp.c
    mpz/tdiv_r_ui.c
    mpz/tstbit.c
    mpz/ui_pow_ui.c
    mpz/ui_sub.c
    mpz/urandomb.c
    mpz/urandomm.c
    mpz/xor.c
)

SET(mpn_SRCS
    mpn/mp_bases.c
    mpn/generic/add.c
    mpn/generic/add_1.c
    mpn/generic/add_n.c
    mpn/generic/addmul_1.c
    mpn/generic/addsub_n.c
    mpn/generic/bdivmod.c
    mpn/generic/cmp.c
    mpn/generic/dc_divrem_n.c
    mpn/generic/dive_1.c
    mpn/generic/diveby3.c
    mpn/generic/divis.c
    mpn/generic/divrem.c
    mpn/generic/divrem_1.c
    mpn/generic/divrem_2.c
    mpn/generic/dump.c
    mpn/generic/fib2_ui.c
    mpn/generic/gcd.c
    mpn/generic/gcd_1.c
    mpn/generic/gcdext.c
    mpn/generic/get_str.c
    mpn/generic/hamdist.c
    mpn/generic/jacbase.c
    mpn/generic/lshift.c
    mpn/generic/mod_1.c
    mpn/generic/mul.c
    mpn/generic/mod_34lsub1.c
    mpn/generic/mode1o.c
    mpn/generic/mul_1.c
    mpn/generic/mul_basecase.c
    mpn/generic/mul_fft.c
    mpn/generic/mul_n.c
    mpn/generic/perfsqr.c
    mpn/generic/popcount.c
    mpn/generic/pow_1.c
    mpn/generic/pre_divrem_1.c
    mpn/generic/pre_mod_1.c
    mpn/generic/random.c
    mpn/generic/random2.c
    mpn/generic/rootrem.c
    mpn/generic/rshift.c
    mpn/generic/sb_divrem_mn.c
    mpn/generic/scan0.c
    mpn/generic/scan1.c
    mpn/generic/set_str.c
    mpn/generic/sizeinbase.c
    mpn/generic/sqr_basecase.c
    mpn/generic/sqrtrem.c
    mpn/generic/sub.c
    mpn/generic/sub_1.c
    mpn/generic/sub_n.c
    mpn/generic/submul_1.c
    mpn/generic/tdiv_qr.c
    mpn/generic/udiv_w_sdiv.c
)

SET(mpq_SRCS
   mpq/abs.c
   mpq/aors.c
   mpq/canonicalize.c
   mpq/clear.c
   mpq/cmp.c
   mpq/cmp_si.c
   mpq/cmp_ui.c
   mpq/div.c
   mpq/equal.c
   mpq/get_d.c
   mpq/get_den.c
   mpq/get_num.c
   mpq/get_str.c
   mpq/init.c
   mpq/inp_str.c
   mpq/inv.c
   mpq/md_2exp.c
   mpq/mul.c
   mpq/neg.c
   mpq/out_str.c
   mpq/set.c
   mpq/set_d.c
   mpq/set_den.c
   mpq/set_f.c
   mpq/set_num.c
   mpq/set_si.c
   mpq/set_str.c
   mpq/set_ui.c
   mpq/set_z.c
   mpq/swap.c
)

SET(printf_SRCS
   printf/asprintf.c
   printf/asprntffuns.c
   printf/doprnt.c
   printf/doprntf.c
   printf/doprnti.c
   printf/fprintf.c
   printf/obprintf.c
   printf/obprntffuns.c
   printf/obvprintf.c
   printf/printf.c
   printf/printffuns.c
   printf/repl-vsnprintf.c
   printf/snprintf.c
   printf/snprntffuns.c
   printf/sprintf.c
   printf/sprintffuns.c
   printf/vasprintf.c
   printf/vfprintf.c
   printf/vprintf.c
   printf/vsnprintf.c
   printf/vsprintf.c
)

SET(scanf_SRCS
   scanf/doscan.c
   scanf/fscanf.c
   scanf/fscanffuns.c
   scanf/scanf.c
   scanf/sscanf.c
   scanf/sscanffuns.c
   scanf/vfscanf.c
   scanf/vscanf.c
   scanf/vsscanf.c
)

# Headers:
# SET(gmp-4.1_executable_HDRS
#     acconfig.h
#     install-sh
#     ltmain.sh
#     mdate-sh
#     gmp-impl.h
#     longlong.h
#     gmpxx.h
#     mpfrxx.h
# )
# 
# SET(gmp-4.1_executable_HDRS
# 	${gmp-4.1_executable_HDRS}
#     mpf/fits_s.h
#     mpf/fits_u.h
# )
# 
# SET(gmp-4.1_executable_HDRS
# 	${gmp-4.1_executable_HDRS}
#     mpz/aors.h
#     mpz/aors_ui.h
#     mpz/fits_s.h
#     mpz/mul_i.h
# )
# 
# SET(gmp-4.1_executable_HDRS
# 	${gmp-4.1_executable_HDRS}
# 	mpn/generic/gmp-mparam.h
# )

SET(HAVE_HOST_CPU_FAMILY_powerpc 0)
SET(HAVE_HOST_CPU_FAMILY_power 0)
#SET(HAVE_HOST_CPU_FAMILY_x86 1)
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
SET(HAVE_NATIVE_mpn_add_nc 1)
SET(HAVE_NATIVE_mpn_sub_nc 1)

if(MSVC)
    SET(inline 1)
endif(MSVC)

CHECK_FUNCTION_EXISTS(alarm HAVE_ALARM)
CHECK_FUNCTION_EXISTS(alloca HAVE_ALLOCA)
CHECK_FUNCTION_EXISTS(clock HAVE_CLOCK)
CHECK_FUNCTION_EXISTS(clock_gettime HAVE_CLOCK_GETTIME)
CHECK_FUNCTION_EXISTS(cputime HAVE_CPUTIME)
CHECK_FUNCTION_EXISTS(vsnprintf HAVE_VSNPRINTF)
CHECK_FUNCTION_EXISTS(times HAVE_TIMES)
CHECK_FUNCTION_EXISTS(memset HAVE_MEMSET)
CHECK_FUNCTION_EXISTS(getpagesize HAVE_GETPAGESIZE)
CHECK_FUNCTION_EXISTS(getrusage HAVE_GETRUSAGE)
CHECK_FUNCTION_EXISTS(gettimeofday HAVE_GETTIMEOFDAY)
CHECK_FUNCTION_EXISTS(localeconv HAVE_LOCALECONV)
CHECK_FUNCTION_EXISTS(lrand48 HAVE_LRAND48)
CHECK_FUNCTION_EXISTS(memset HAVE_MEMSET)
CHECK_FUNCTION_EXISTS(mmap HAVE_MMAP)
CHECK_FUNCTION_EXISTS(obstack_vprintf HAVE_OBSTACK_VPRINTF)
CHECK_FUNCTION_EXISTS(popen HAVE_POPEN)
CHECK_FUNCTION_EXISTS(processor_info HAVE_PROCESSOR_INFO)
CHECK_FUNCTION_EXISTS(read_real_time HAVE_READ_REAL_TIME)
CHECK_FUNCTION_EXISTS(sigaction HAVE_SIGACTION)
CHECK_FUNCTION_EXISTS(sigaltstack HAVE_SIGALTSTACK)
CHECK_FUNCTION_EXISTS(sigstack HAVE_SIGSTACK)
CHECK_FUNCTION_EXISTS(strnlen HAVE_STRNLEN)
CHECK_FUNCTION_EXISTS(strcasecmp HAVE_STRCASECMP)
CHECK_FUNCTION_EXISTS(strchr HAVE_STRCHR)

CHECK_INCLUDE_FILES(alloca.h HAVE_ALLOCA_H)
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
CHECK_INCLUDE_FILES(dlfcn.h HAVE_DLFCN_H)
CHECK_INCLUDE_FILES(fcntl.h HAVE_FCNTL_H)
CHECK_INCLUDE_FILES(fpu_control.h HAVE_FPU_CONTROL_H)
CHECK_INCLUDE_FILES(inttypes.h HAVE_INTTYPES_H)
CHECK_INCLUDE_FILES(locale.h HAVE_LOCALE_H)
CHECK_INCLUDE_FILES(memory.h HAVE_MEMORY_H)
CHECK_INCLUDE_FILES(stdint.h HAVE_STDINT_H)
#CHECK_INCLUDE_FILES(stdlib.h HAVE_STDLIB_H)
#CHECK_INCLUDE_FILES(strings.h HAVE_STRINGS_H)
#CHECK_INCLUDE_FILES(string.h HAVE_STRING_H)

CHECK_C_SOURCE_COMPILES("int foo (int x) __attribute__ ((const));int main () {}", HAVE_ATTRIBUTE_CONST)
CHECK_C_SOURCE_COMPILES("void foo (int x) __attribute__ ((malloc));int main () {}", HAVE_ATTRIBUTE_MALLOC)
CHECK_C_SOURCE_COMPILES("typedef int SItype __attribute__ ((mode (SI)));int main () {}", HAVE_ATTRIBUTE_MODE)
CHECK_C_SOURCE_COMPILES("void foo (int x) __attribute__ ((noreturn));int main () {}", HAVE_ATTRIBUTE_NORETURN)


SET(CMAKE_EXTRA_INCLUDE_FILES stdint.h)
CHECK_TYPE_SIZE("intmax_t" INTMAX_T)
SET(CMAKE_EXTRA_INCLUDE_FILES)
CHECK_TYPE_SIZE("long double" LONG_DOUBLE)
CHECK_TYPE_SIZE("long long" LONG_LONG)
CHECK_TYPE_SIZE("long long" PTRDIFF_T)
SET(CMAKE_EXTRA_INCLUDE_FILES stddef.h)
CHECK_TYPE_SIZE("ptrdiff_t" PTRDIFF_T)
SET(CMAKE_EXTRA_INCLUDE_FILES)

#we should choose the right gmp-mparam by the type of processor but I don't know how to do that
CONFIGURE_FILE(mpn/x86/p6/gmp-mparam.h ${CMAKE_BINARY_DIR}/gmp-mparam.h COPYONLY)
CONFIGURE_FILE(stamp-h1.in ${CMAKE_BINARY_DIR}/stamp.h1)
#CONFIGURE_FILE(Makefile.in ${CMAKE_BINARY_DIR}/Makefile)
CONFIGURE_FILE(config.in ${CMAKE_BINARY_DIR}/config.h)
#CONFIGURE_FILE(configure.in ${CMAKE_BINARY_DIR}/configure)
CONFIGURE_FILE(gmp-h.in ${CMAKE_BINARY_DIR}/gmp.h)
CONFIGURE_FILE(mp-h.in ${CMAKE_BINARY_DIR}/mp.h)


add_definitions(-DHAVE_CONFIG_H -D__GMP_WITHIN_GMP)

# actual target:
ADD_LIBRARY(mpf STATIC ${mpf_SRCS})
# set_target_properties(mpf PROPERTIES DEFINE_SYMBOL __GMP_WITHIN_GMP)

ADD_LIBRARY(mpz STATIC ${mpz_SRCS})
# set_target_properties(mpz PROPERTIES DEFINE_SYMBOL __GMP_WITHIN_GMP)

ADD_LIBRARY(mpn STATIC ${mpn_SRCS})
# set_target_properties(mpf PROPERTIES DEFINE_SYMBOL __GMP_WITHIN_GMP)

ADD_LIBRARY(mpq STATIC ${mpq_SRCS})
# set_target_properties(mpq PROPERTIES DEFINE_SYMBOL __GMP_WITHIN_GMP)

ADD_LIBRARY(printf STATIC ${printf_SRCS})
# set_target_properties(printf PROPERTIES DEFINE_SYMBOL __GMP_WITHIN_GMP)

ADD_LIBRARY(scanf STATIC ${scanf_SRCS})
# set_target_properties(scanf PROPERTIES DEFINE_SYMBOL __GMP_WITHIN_GMP)

ADD_LIBRARY(gmp SHARED ${gmp-4.1_executable_SRCS})
# set_target_properties(gmp-4.1 PROPERTIES DEFINE_SYMBOL __GMP_WITHIN_GMP)
target_link_libraries(gmp mpf mpz mpn mpq printf scanf)
# add install target:
install(TARGETS gmp
                RUNTIME DESTINATION bin
                LIBRARY DESTINATION lib
                ARCHIVE DESTINATION lib
)

install(FILES ${CMAKE_CURRENT_BINARY_DIR}/gmp.h          DESTINATION include)
