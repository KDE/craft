# -*- coding: utf-8 -*-
# this package contains functions to check the current compiler
# copyright:
# Patrick von Reth <patrick.vonreth [AT] gmail [DOT] com>

"""@package provides boost build system"""

import os
import utils
from BuildSystem.BuildSystemBase import *

class BoostBuildSystem(BuildSystemBase):
    """ cmake build support """
    def __init__( self ):
        """constructor. configureOptions are added to the configure command line and makeOptions are added to the make command line"""
        BuildSystemBase.__init__(self, "boost")

    def configureOptions( self, defines=""):
        """returns default configure options"""
        options = BuildSystemBase.configureOptions(self)              
        options += (" --build-type=minimal"
                " --build-dir=" + self.buildDir() + \
                " threading=multi"
                " link=shared"
                " runtime-link=shared")

        options += " variant="
        if self.buildType() == "Debug":
            options += "debug"
        else:
            options += "release"
        options += " toolset="
        if compiler.isMinGW():
            options += "gcc"
        else:
            if compiler.isMSVC2005():
                options += "msvc-8.0"
            elif compiler.isMSVC2008():
                options += "msvc-9.0"
            elif compiler.isMSVC2010():
                options += "msvc-10.0"    
        return options

    def configure( self, defines=""):
        return True

    def make( self ):
        """implements the make step for cmake projects"""
        self.boost = portage.getPackageInstance('win32libs-sources', 'boost-src')
        self.subinfo.targetInstSrc[ self.subinfo.buildTarget ] = os.path.join(self.boost.sourceDir(),"libs",self.subinfo.targetInstSrc[ self.subinfo.buildTarget ],"build")
        
        self.enterSourceDir()
        cmd  = "bjam"
        cmd += self.configureOptions(self.subinfo.options.configure.defines)
        if utils.verbose() >= 1:
            print cmd
        os.system(cmd) and utils.die(
                "command: %s failed" % (cmd))
        return True



    def _walk(self, directory,ending):
        for f in os.listdir(directory):
          path = os.path.join(directory,f)
          if os.path.isdir(path):
              return self._walk(path,ending)
          elif f.endswith(ending):
              return directory,f
              
    def install( self):
        """install the target"""
        try:
          path,dll = self._walk(self.buildDir(),"dll")
        except Exception:
          utils.die("Build Failed")
        utils.copyFile(os.path.join(path,dll),os.path.join(self.imageDir(),"lib",dll))
        utils.copyFile(os.path.join(path,dll),os.path.join(self.imageDir(),"bin",dll))
        if compiler.isMinGW():
            lib = dll + ".a"
        elif compiler.isMSVC():
          lib = dll[0:-3] + "lib"
        utils.copyFile(os.path.join(path,lib),os.path.join(self.imageDir(),"lib",lib))
        return True

    def unittest( self ):
        return True


