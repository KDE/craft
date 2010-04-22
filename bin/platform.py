# -*- coding: utf-8 -*-
"""@brief plaftorm settings
this file contains some compiling platform/arch functions for emerge
"""

# copyright:
# Romain Pokrzywka <romain [AT] kdab [DOT] com>

import os

def buildArchitecture():
    """return the compiling CPU architecture."""
    return os.getenv( "EMERGE_ARCHITECTURE" )

def targetPlatform():
    """return the cross-compiling target platform."""
    return os.getenv( "EMERGE_TARGET_PLATFORM" )

def targetArchitecture():
    """return the cross-compiling target CPU architecture."""
    return os.getenv( "EMERGE_TARGET_ARCHITECTURE" )

def isCrossCompilingEnabled():
    """define if cross-compiling is enabled"""
    return targetPlatform() != None and targetPlatform() != ""

