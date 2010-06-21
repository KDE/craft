# -*- coding: utf-8 -*-
# this package contains functions to use cach compilers
# copyright:
# Patrick von Reth <patrick.vonreth [AT] gmail [DOT] com>

import os
import utils
import compiler



if os.getenv("EMERGE_USE_CCACHE") == "True" and compiler.isMinGW():
  utils.putenv( "CCACHE_DIR" , os.path.join( os.getenv("KDEROOT") , "build" , "CCACHE" ) )
  if int(os.getenv("EMERGE_VERBOSE")) > 1:
    utils.putenv( "CCACHE_LOGFILE" , os.path.join( str(os.getenv("CCACHE_DIR")) , "ccachelog.txt" ) )

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
    os.putenv("CXX" , "ccache g++" )
    os.putenv("CC" , "ccache gcc" )
    return " -e "
   
  return ""


 