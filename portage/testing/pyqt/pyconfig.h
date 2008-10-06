
// debug builds of python library provides additional functions not available in the release build. 
// Because building python on windows is a nightmare yet (no cmake support)  we are tight to the 
// python release build also for PyQt debug builds. To avoid unresolved symbols while linking 
// we have to undefine Py_DEBUG.

#include <../include/pyconfig.h>
#ifdef _DEBUG
#undef Py_DEBUG
#endif
