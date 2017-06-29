# -*- coding: utf-8 -*-
# this package contains functions to check the current compiler
# copyright:
# Hannah von Reth <vonreth@kde.org>

import os
import subprocess
import re

from CraftDebug import craftDebug
import utils
from CraftConfig import *




def _getGCCTarget():
    result = utils.utilsCache.getCommandOutput("gcc", "-dumpmachine")
    if result:
        result = result.strip()
        craftDebug.log.debug(f"GCC Target Processor: {result}")
    else:
        #if no mingw is installed return mingw-w32 it is part of base
        if isX64():
            result = "x86_64-w64-mingw32"
        else:
            result = "i686-w64-mingw32"
    return result

def architecture():
    return craftSettings.get("General", "Architecture" )

def isNative():
    return craftSettings.getboolean("General", "Native", True)

def isX64():
    return architecture() == "x64"

def isX86():
    return architecture() == "x86"


def _compiler():
    return craftSettings.get("General","KDECOMPILER")

def isGCC():
    return isMinGW() or _compiler().endswith("-gcc")

def isClang():
    return _compiler().endswith("-clang")

def isGCCLike():
    return (isGCC() or isClang())

def isMinGW():
    return _compiler().startswith("mingw")

def isMinGW_W32():
    return isMinGW() and _getGCCTarget() == "i686-w64-mingw32"

def isMinGW_W64():
    return isMinGW() and isX64()

def isMSVC():
    return _compiler().startswith("msvc")

def isMSVC2010():
    return _compiler() == "msvc2010"

def isMSVC2012():
    return _compiler() == "msvc2012"

def isMSVC2013():
    return _compiler() == "msvc2013"

def isMSVC2015():
    return _compiler() == "msvc2015"

def isMSVC2017():
    return _compiler() == "msvc2017"

def isIntel():
    return _compiler() == "intel"

def getCompilerExecutableName():
    if isGCC():
        return "gcc"
    elif isClang():
        return "clang"
    elif isMSVC():
        return "cl"
    else:
        craftDebug.log.critical(f"Unsupported Compiler {_compiler()}")

def getCompilerName():
    if isMinGW():
        return "mingw-w64"
    elif isMSVC():
        return _compiler()
    elif isIntel():
        return "intel-%s-%s" % (os.getenv("TARGET_ARCH"), os.getenv("TARGET_VS"))
    elif isGCC():
        return "gcc"
    elif isClang():
        return "clang"
    else:
        craftDebug.log.critical("Unknown Compiler %s" % _compiler())

def getSimpleCompilerName():
    if isMinGW():
        return "mingw64"
    elif isMSVC():
        return "msvc"
    elif isIntel():
        return "intel"
    else:
        return getCompilerName()

def getGCCLikeVersion(compilerExecutable):
    result = utils.utilsCache.getCommandOutput(compilerExecutable, "--version")
    if result:
        result = re.findall("\d+\.\d+\.?\d*",result)[0]
        craftDebug.log.debug("{0} Version: {1}".format(compilerExecutable, result))
    return result or "0"

def getVersion():
    if isGCCLike():
        return f"{getCompilerName()} {getGCCLikeVersion(getCompilerExecutableName())}"
    elif isIntel():
        return os.getenv("PRODUCT_NAME_FULL")
    elif isMSVC():
        return "Microsoft Visual Studio 20%s" %  _compiler()[len(_compiler())-2:]
    else:
        return None
    
def getShortName():
    if not isMSVC():
        return getCompilerName()
    return f"vc{internalVerison()}"


def internalVerison():
    if not isMSVC():
        return getVersion()
    versions = {
        "msvc2010": 10,
        "msvc2012": 11,
        "msvc2013": 12,
        "msvc2015": 14,
        "msvc2017": 15
    }
    if _compiler() not in versions:
        craftDebug.log.critical(f"Unknown MSVC Compiler {_compiler()}")
    return versions[_compiler()]


def msvcPlatformToolset():
    versions = {
        "msvc2010": 100,
        "msvc2012": 110,
        "msvc2013": 120,
        "msvc2015": 140,
        "msvc2017": 141
    }
    if _compiler() not in versions:
        craftDebug.log.critical(f"Unknown MSVC Compiler {_compiler()}")
    return versions[_compiler()]

if __name__ == '__main__':
    print("Testing Compiler.py")
    print("Configured compiler (KDECOMPILER): %s" % _compiler())
    print("Version: %s" % getVersion())
    print("Compiler Name: %s" % getCompilerName())
    print("Native compiler: %s" % ("No", "Yes")[isNative()])
    if isGCCLike():
        print("Compiler Version: %s" % getGCCLikeVersion(getCompilerExecutableName()))
        print("Compiler Target: %s" % _getGCCTarget())
