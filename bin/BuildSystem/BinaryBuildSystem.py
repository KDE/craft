# 
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
# installing binary packages 

import os
import utils

import base
import info

from BuildSystemBase import *

class BinaryBuildSystem(BuildSystemBase):
    def __init__( self):
        BuildSystemBase.__init__(self,"binary","BinaryBuildSystem")
        
    def configure( self ):
        return True

    def make( self ):
        return True

    # nothing to do - unpack hasd done this job already
    def install( self ):
        return True
        
    def runTest( self ):
        return False