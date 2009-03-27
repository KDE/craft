project(samplerate)

set (VERSION_MAJOR 0)
set (VERSION_MINOR 1)
set (VERSION_PATH 7)

cmake_minimum_required(VERSION 2.6)

include_directories(
	Win32
)
	
set (COEFF_HDRS 
	src/fastest_coeffs.h 
	src/mid_qual_coeffs.h 
	src/high_qual_coeffs.h
)

set (SRC_SOURCES 
	src/samplerate.c 
	src/src_sinc.c 
	src/src_zoh.c 
	src/src_linear.c
	${COEFF_HDRS}
)

add_library(samplerate ${SRC_SOURCES}) 
set_target_properties(samplerate PROPERTIES LINK_FLAGS "/def:${CMAKE_SOURCE_DIR}/Win32/libsamplerate-${VERSION_MAJOR}.def")
set_target_properties(samplerate PROPERTIES OUTPUT_NAME "samplerate-${VERSION_MAJOR}")
target_link_libraries(samplerate)

install(TARGETS samplerate RUNTIME DESTINATION bin ARCHIVE DESTINATION lib LIBRARY DESTINATION lib)
install(FILES src/samplerate.h DESTINATION include)

#include_HEADERS = samplerate.h

#EXTRA_DIST = config.h.in Version_script.in check_asm.sh
#CLEANFILES = src_sinc.s

#-------------------------------------------------------------------------------
# An extra check for bad asm.
#check-asm : check_asm.sh src_sinc.s src_linear.s src_zoh.s
#	@echo
#	@echo
#	$(srcdir)/check_asm.sh src_sinc.s
#	$(srcdir)/check_asm.sh src_linear.s
#	$(srcdir)/check_asm.sh src_zoh.s
#	@echo
#	@echo

#%.s : $(srcdir)/%.c
#	$(CC) -S $(CFLAGS) $(DEFAULT_INCLUDES) $(srcdir)/$+ -o $@

## Disable autoheader.
#AUTOHEADER=echo

