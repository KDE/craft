# -*- coding: utf-8 -*-
# this package contains functions to check the current compiler
# copyright:
# Patrick von Reth <patrick.vonreth [AT] gmail [DOT] com>

import os
import utils
import subprocess

COMPILER=os.getenv("KDECOMPILER")

def getGCCTarget():
    if not isMinGW():
        return False
   # FIXME: This is broken because the invariant that a compiler is installed is
   # not fulfilled at every time especially when building the dependency tree
   result = subprocess.Popen("gcc -dumpmachine", stdout=subprocess.PIPE).communicate()[0]
   utils.debug("GCC Target Processor:%s" % result, 1 )
   return result.strip()

def isMinGW():
    return COMPILER.startswith("mingw")

def isMinGW32():
    return getGCCTarget() == "mingw32"

def isMinGW_WXX():
    return isMinGW() and not isMinGW32()

def isMinGW_W32():
    return getGCCTarget() == "i686-w64-mingw32"

def isMinGW_W64():
    return getGCCTarget() == "x86_64-w64-mingw32"


def isMSVC():
    return COMPILER.startswith("msvc")

def isMSVC2008():
    return COMPILER == "msvc2008"

def isMSVC2005():
    return COMPILER == "msvc2005"

def getCompilerName():
    if isMinGW():
        if isMinGW_W32():
            return "mingw-w32"
     elif isMinGW_W64():
         return "mingw-w64"
     elif isMinGW32():
         return "mingw32"
   elif isMSVC():
       return COMPILER
   else:
       return "Unknown Compiler"

def getSimpleCompilerName():
    if isMinGW():
        if isMinGW_W64():
            return "mingw64"
     else:
         return "mingw"
   elif isMSVC():
       return "msvc"
   else:
       return "Unknown Compiler"
