# -*- coding: utf-8 -*-
# this package contains functions to check the current compiler
# copyright:
# Patrick von Reth <patrick.vonreth [AT] gmail [DOT] com>

import os
import utils
import subprocess
import emergePlatform

COMPILER = os.getenv("KDECOMPILER")
GCCTARGET = None
MINGW_VERSION = None

def getGCCTarget():
    global GCCTARGET # pylint: disable=W0603
    if not GCCTARGET:
        try:
            result = str(subprocess.Popen("gcc -dumpmachine", stdout=subprocess.PIPE).communicate()[0],'windows-1252')
            utils.debug("GCC Target Processor:%s" % result, 1 )
            GCCTARGET = result.strip()
        except OSError:
            #if no mingw is installed return mingw-w32 it is part of base
            GCCTARGET = "i686-w64-mingw32"
    return GCCTARGET

def isMinGW():
    return COMPILER.startswith("mingw")

def isMinGW32():
    return isMinGW() and getGCCTarget() == "mingw32"

def isMinGW_WXX():
    return isMinGW_W32() or isMinGW_W64()

def isMinGW_W32():
    return isMinGW() and getGCCTarget() == "i686-w64-mingw32"

def isMinGW_W64():
    return isMinGW() and emergePlatform.buildArchitecture() == "x64"

def isMinGW_ARM():
    return isMinGW() and emergePlatform.buildArchitecture() == 'arm-wince'


def isMSVC():
    return COMPILER.startswith("msvc")

def isMSVC2005():
    return COMPILER == "msvc2005"

def isMSVC2008():
    return COMPILER == "msvc2008"

def isMSVC2010():
    return COMPILER == "msvc2010"

def isMSVC2011():
    return COMPILER == "msvc2011"


def getCompilerName():
    if isMinGW():
        if isMinGW_W32():
            return "mingw-w32"
        elif isMinGW_W64():
            return "mingw-w64"
        elif isMinGW32():
            return "mingw32"
        elif isMinGW_ARM():
            return "arm-wince"
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

def getMinGWVersion():
    global MINGW_VERSION # pylint: disable=W0603
    if not MINGW_VERSION:
        try:
            result = str(subprocess.Popen("gcc --version", stdout=subprocess.PIPE).communicate()[0],'windows-1252')
            result = result.split()[2]
            utils.debug("GCC Version:%s" % result, 1 )
            MINGW_VERSION = result.strip()
        except OSError:
            #if no mingw is installed return 0
            MINGW_VERSION = "0"
    return MINGW_VERSION

def getVersion():
    if isMinGW():
        return "%s %s" % ( getCompilerName(), getMinGWVersion() )
    return "Microsoft Visual Studio 20%s" %  COMPILER[len(COMPILER)-2:]


if __name__ == '__main__':
    print("Testing Compiler.py")
    print("Version: %s" % getVersion())
    print("Compiler Name: %s" % getCompilerName())

