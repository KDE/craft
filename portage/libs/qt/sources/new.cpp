#include <exception> // for std::bad_alloc
#include <new>
#if 1
#include "qplatformdefs.h"
#else
#define qFree free
#define qMalloc malloc
#include <stdlib.h>
#endif

using namespace std;

void* operator new (size_t size) throw (bad_alloc)
{
  void* ptr = qMalloc(size);
  if (ptr == 0)
    throw bad_alloc();
  return ptr;
}

void* operator new[] (size_t size) throw (bad_alloc)
{
  void* ptr = qMalloc(size);
  if (ptr == 0)
    throw bad_alloc();
  return ptr;
}

void operator delete (void* ptr) throw()
{
  qFree (ptr);
}

void operator delete[] (void* ptr) throw()
{
  qFree (ptr);
}

void* operator new (size_t size, const nothrow_t& dummy) throw()
{
  return qMalloc(size);
}

void* operator new[] (size_t size, const nothrow_t& dummy) throw()
{
  return qMalloc(size);
}

void operator delete(void* ptr, const nothrow_t& dummy) throw()
{
  qFree (ptr);
}

void operator delete[](void* ptr, const nothrow_t& dummy) throw()
{
  qFree (ptr);
}
