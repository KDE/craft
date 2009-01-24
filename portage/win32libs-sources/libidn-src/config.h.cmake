#define PACKAGE "@PACKAGE_VERSION@"
#define PACKAGE_NAME "@PACKAGE_NAME@"
#define PACKAGE_VERSION "@PACKAGE_VERSION@"
#define PACKAGE_BUGREPORT "@PACKAGE_BUGREPORT@"
#define VERSION "@PACKAGE_VERSION@"
#define LOCALEDIR "@LOCALEDIR@"

#ifdef WIN32
#define strcasecmp stricmp
#define strncasecmp strnicmp
#endif

#if _MSC_VER && !__cplusplus
# define inline __inline
#endif

