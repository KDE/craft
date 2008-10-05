
// In debug builds some  functions are required which are not provided by the release python installation 
// To avoid the need for building python debug libraries undefine Py_Debug
#include <../include/pyconfig.h>
#ifdef _DEBUG
#undef Py_Debug
#endif

