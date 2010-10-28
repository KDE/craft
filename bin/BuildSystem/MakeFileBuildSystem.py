# 
# copyright (c) 2010 Ralf Habacker <ralf.habacker@freenet.de>
#

"""@package provides simple makefile based build system without any configure step"""

import os
import utils

import base
import info

from BuildSystemBase import *

class MakeFileBuildSystem(BuildSystemBase):
    """ make file build support """
    def __init__( self ):
        """constructor. configureOptions are added to the configure command line and makeOptions are added to the make command line"""
        BuildSystemBase.__init__(self,"makefile","MakeFileBuildSystem")

    def configure( self, defines=""):
        """implements configure step for cmake projects"""

        return True

    def make( self ):
        """implements the make step for Makefile projects"""

        self.enterBuildDir()
        if self.envPath <> '':
            utils.debug("adding %s to system path" % os.path.join( self.rootdir, self.envPath ),2)
            os.putenv( "PATH", os.path.join( self.rootdir, self.envPath ) + ";" + os.getenv("PATH") )

        command = self.makeProgramm

        if utils.verbose() > 1:
            command += " VERBOSE=1"
        
        if self.subinfo.options.make.ignoreErrors:
            command += " -i"
            
        if self.subinfo.options.make.makeOptions:
            command += " %s" % self.subinfo.options.make.makeOptions

        return self.system( command, "make" ) 
        
    def install( self):
        """install the target"""
        self.enterBuildDir()
        command = "%s install DESTDIR=%s" % (self.makeProgramm, self.installDir())        
        self.system( command, "install" ) 
        return True

    def unittest( self ):
        """running make tests"""

        self.enterBuildDir()

        return self.system( "%s test" % ( self.makeProgramm ), "test" )
