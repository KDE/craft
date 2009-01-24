project(libcurl)
cmake_minimum_required(VERSION 2.6.2)
# this is just a simple makefile to build libcurl. A proper CMakeLists.txt
# should be made and then send to curl maintainer

#-------------------------------------------------------------------
# LIBCURL
#-------------------------------------------------------------------
set(curl_SOURCES
    lib/base64.c
    lib/connect.c
    lib/content_encoding.c
    lib/cookie.c
    lib/curl_addrinfo.c
    lib/dict.c
    lib/easy.c
    lib/escape.c
    lib/file.c
    lib/formdata.c
    lib/ftp.c
    lib/getenv.c
    lib/getinfo.c
    lib/gtls.c
    lib/hash.c
    lib/hostares.c
    lib/hostasyn.c
    lib/hostip.c
    lib/hostip4.c
    lib/hostip6.c
    lib/hostsyn.c
    lib/hostthre.c
    lib/http.c
    lib/http_chunks.c
    lib/http_digest.c
    lib/http_negotiate.c
    lib/http_ntlm.c
    lib/if2ip.c
    lib/inet_ntop.c
    lib/inet_pton.c
    lib/krb4.c
    lib/krb5.c
    lib/ldap.c
    lib/llist.c
    lib/md5.c
    lib/memdebug.c
    lib/mprintf.c
    lib/multi.c
    lib/netrc.c
    lib/nss.c
    lib/parsedate.c
    lib/progress.c
    lib/qssl.c
    lib/rawstr.c
    lib/security.c
    lib/select.c
    lib/sendf.c
    lib/share.c
    lib/socks.c
    lib/speedcheck.c
    lib/splay.c
    lib/ssh.c
    lib/sslgen.c
    lib/ssluse.c
    lib/strdup.c
    lib/strequal.c
    lib/strerror.c
    lib/strtok.c
    lib/strtoofft.c
    lib/telnet.c
    lib/tftp.c
    lib/timeval.c
    lib/transfer.c
    lib/url.c
    lib/version.c
)
set(curl_HEADERS
    include/curl/curl.h
    include/curl/curlbuild.h
    include/curl/curlrules.h
    include/curl/curlver.h
    include/curl/easy.h
    include/curl/mprintf.h
    include/curl/multi.h
    include/curl/stdcheaders.h
    include/curl/types.h
    include/curl/typecheck-gcc.h
)

add_definitions(-DBUILDING_LIBCURL)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)
add_library(curl SHARED ${curl_SOURCES} ${curl_HEADERS})
if(WIN32)
  target_link_libraries(curl ws2_32 wldap32)
endif(WIN32)
if(WIN32)
  set_target_properties(curl PROPERTIES OUTPUT_NAME libcurl)
endif(WIN32)

install(TARGETS curl RUNTIME DESTINATION bin ARCHIVE DESTINATION lib)
install(FILES   ${curl_HEADERS} DESTINATION include/curl)
