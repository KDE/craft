# -*- coding: utf-8 -*-
# this package contains functions to use cach compilers
# copyright:
# Patrick von Reth <patrick.vonreth [AT] gmail [DOT] com>

import os
import utils
import compiler



if os.getenv("EMERGE_USE_CCACHE") == "True" and compiler.isMinGW():
  os.putenv("CCACHE_DIR",os.path.join(os.getenv("KDEROOT") , "build" , "CCACHE" ) )

def getCMakeArguments():
  if os.getenv("EMERGE_USE_CCACHE") == "True" and compiler.isMinGW():
    return " -DCMAKE_CXX_COMPILER=ccache -DCMAKE_CXX_COMPILER_ARG1=g++ -DCMAKE_C_COMPILER=ccache -DCMAKE_C_COMPILER_ARG1=gcc "
    
  return ""



def getMsysMakeArguments():
  if os.getenv("EMERGE_USE_CCACHE") == "True" and compiler.isMinGW():
    return " CXX=\'ccache g++\' CC=\'ccache gcc\' "
    
  return ""

def getQmakeMakeArguments():
  if os.getenv("EMERGE_USE_CCACHE") == "True" and compiler.isMinGW():
    ccache = os.path.join( os.getenv( "KDEROOT" ) , "bin" , "ccache.exe" )
    os.putenv("CXX" , "%s g++" % ccache )
    os.putenv("CC" , "%s gcc" % ccache )
    return " -e "
   
  return ""


 