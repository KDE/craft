project(gmm)

# the following are directories where stuff will be installed to
set(INCLUDE_INSTALL_DIR      "${CMAKE_INSTALL_PREFIX}/include"             CACHE PATH "The subdirectory to the header prefix" FORCE)

FILE(GLOB gmm_header_SRCS "include/gmm/*.h")

install(FILES 
  ${gmm_header_SRCS}
  DESTINATION ${INCLUDE_INSTALL_DIR}/gmm
  )

