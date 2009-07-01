# -*- coding: utf-8 -*-
# installing binary packages 

import os
import utils

import base
import info

from BuildSystemBase import *

class BinaryBuildSystem(BuildSystemBase):
    def __init__( self, env = dict( os.environ ) ):
        BuildSystemBase.__init__(self)
        
    def configure( self, buildType=None, customOptions="" ):
        return True

    def make( self, buildType=None ):
        return True

    # nothing to do - unpack hasd done this job already
    def install( self, buildType=None ):
        return True
        
    def runTest( self ):
        return False