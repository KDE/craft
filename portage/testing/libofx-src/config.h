// Have these
#define HAVE_EVENTGENERATOR_H 1
#define HAVE_LIBCURL 1
#define HAVE_MEMORY_H 1
#define HAVE_PARSEREVENTGENERATORKIT_H 1
#define HAVE_SGMLAPPLICATION_H 1
#define HAVE_STDLIB_H 1
#define HAVE_STRING_H 1
#define HAVE_SYS_STAT_H 1
#define HAVE_SYS_TYPES_H 1

// Do not exist
#undef HAVE_DLFCN_H
#undef HAVE_GETOPT_H
#undef HAVE_GETOPT_LONG
#undef HAVE_INTTYPES_H
#undef HAVE_STDINT_H
#undef HAVE_STRINGS_H
#undef HAVE_UNISTD_H


// Unsure
#define HAVE_ICONV 1
#define HAVE_LIBXMLPP 1

#undef LIBCURL_FEATURE_ASYNCHDNS

/* Defined if libcurl supports IPv6 */
#undef LIBCURL_FEATURE_IPV6

/* Defined if libcurl supports KRB4 */
#undef LIBCURL_FEATURE_KRB4

/* Defined if libcurl supports libz */
#undef LIBCURL_FEATURE_LIBZ

/* Defined if libcurl supports SSL */
#undef LIBCURL_FEATURE_SSL

/* Defined if libcurl supports DICT */
#undef LIBCURL_PROTOCOL_DICT

/* Defined if libcurl supports FILE */
#undef LIBCURL_PROTOCOL_FILE

/* Defined if libcurl supports FTP */
#undef LIBCURL_PROTOCOL_FTP

/* Defined if libcurl supports FTPS */
#undef LIBCURL_PROTOCOL_FTPS

/* Defined if libcurl supports GOPHER */
#undef LIBCURL_PROTOCOL_GOPHER

/* Defined if libcurl supports HTTP */
#undef LIBCURL_PROTOCOL_HTTP

/* Defined if libcurl supports HTTPS */
#undef LIBCURL_PROTOCOL_HTTPS

/* Defined if libcurl supports LDAP */
#undef LIBCURL_PROTOCOL_LDAP

/* Defined if libcurl supports TELNET */
#undef LIBCURL_PROTOCOL_TELNET


// MSVC Defines we seem to need
#ifdef _MSC_VER
typedef int ssize_t;
#endif
