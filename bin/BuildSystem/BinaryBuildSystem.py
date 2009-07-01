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
        return 

    def make( self, buildType=None ):
        return

    def install( self, buildType=None ):
        enterBuildDir()
        print "unpack archive file"
        # unpack archive file into image directory
        return True

    def runTest( self ):
        return