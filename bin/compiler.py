# -*- coding: utf-8 -*-
# this package contains functions to check the current compiler
# copyright:
# Patrick von Reth <patrick.vonreth [AT] gmail [DOT] com>

import os
import subprocess
import re

import utils
from EmergeConfig import *



_GCCTARGET = None
_MINGW_VERSION = None

def _getGCCTarget():
    global _GCCTARGET # pylint: disable=W0603
    if not _GCCTARGET:
        status, result = subprocess.getstatusoutput("gcc -dumpmachine")
        if status == 0:
            utils.debug("GCC Target Processor:%s" % result, 1 )
            _GCCTARGET = result.strip()
        else:
            #if no mingw is installed return mingw-w32 it is part of base
            if isX64():
                _GCCTARGET = "x86_64-w64-mingw32"
            else:
                _GCCTARGET = "i686-w64-mingw32"
    return _GCCTARGET

def architecture():
    return emergeSettings.get("General", "EMERGE_ARCHITECTURE" )

def isX64():
    return architecture() == "x64"

def isX86():
    return architecture() == "x86"


def _compiler():
    return emergeSettings.get("General","KDECOMPILER")

def isMinGW():
    return _compiler().startswith("mingw")

def isMinGW_W32():
    return isMinGW() and _getGCCTarget() == "i686-w64-mingw32"

def isMinGW_W64():
    return isMinGW() and isX64()

def isMSVC():
    return _compiler().startswith("msvc")

def isMSVC2005():
    return _compiler() == "msvc2005"

def isMSVC2008():
    return _compiler() == "msvc2008"

def isMSVC2010():
    return _compiler() == "msvc2010"

def isMSVC2012():
    return _compiler() == "msvc2012"
    
def isMSVC2013():
    return _compiler() == "msvc2013"

def isIntel():
    return _compiler() == "intel"

def getCompilerName():
    if isMinGW():
        if isMinGW_W32():
            return "mingw-w32"
        elif isMinGW_W64():
            return "mingw-w64"
    elif isMSVC():
        return _compiler()
    elif isIntel():
        return "intel-%s-%s" % (os.getenv("TARGET_ARCH"), os.getenv("TARGET_VS"))
    else:
        utils.die("Unknown Compiler %s" %  _compiler())

def getSimpleCompilerName():
    if isMinGW():
        if isMinGW_W64():
            return "mingw64"
        else:
            return "mingw"
    elif isMSVC():
        return "msvc"
    elif isIntel():
        return "intel"
    else:
        utils.die("Unknown Compiler %s" %  _compiler())

def getMinGWVersion():
    global _MINGW_VERSION # pylint: disable=W0603
    if not _MINGW_VERSION:
        status, result = subprocess.getstatusoutput("gcc --version")
        if status == 0:
            result = re.findall("\d+\.\d+\.?\d*",result)[0]
            utils.debug("GCC Version:%s" % result, 1 )
            _MINGW_VERSION = result.strip()
        else:
            #if no mingw is installed return 0
            _MINGW_VERSION = "0"
    return _MINGW_VERSION

def getVersion():
    if isMinGW():
        return "%s %s" % ( getCompilerName(), getMinGWVersion() )
    elif isIntel():
        return os.getenv("PRODUCT_NAME_FULL")
    return "Microsoft Visual Studio 20%s" %  _compiler()[len(_compiler())-2:]
    
def getShortName():
    if isMinGW():
        return "mingw4"
    elif isMSVC2008():
        return "vc90"
    elif isMSVC2010():
        return "vc100"
    elif isMSVC2012():
        return "vc110"
    elif isMSVC2013():
        return "vc120"
    else:
        utils.die("Unknown Compiler %s" %  _compiler())


if __name__ == '__main__':
    print("Testing Compiler.py")
    print("Version: %s" % getVersion())
    print("Compiler Name: %s" % getCompilerName())
    print("Compiler Version: %s" % getMinGWVersion())

