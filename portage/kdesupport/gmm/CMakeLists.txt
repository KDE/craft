project(gmm)

FILE(GLOB gmm_header_SRCS "include/gmm/*.h")

install(FILES 
  ${gmm_header_SRCS}
  DESTINATION include/gmm
  )

