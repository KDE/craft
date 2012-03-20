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

    def configureOptions( self, defines="" ):
        """returns default configure options"""
        options = BuildSystemBase.configureOptions(self)
        options += (" --build-type=minimal"
#                " --debug-configuration"
                " --build-dir=" + self.buildDir() + \
                " threading=multi")
                
        if not utils.varAsBool(self.subinfo.options.buildStatic):
            options += " link=shared"
                       " runtime-link=shared")
        else:
            options += " link=static"
                       " runtime-link=static")

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
        emergeUserConfig = os.path.join( os.getenv( "KDEROOT" ), "etc", "emerge-boost-config.jam" )
        if os.path.exists( emergeUserConfig ):
            options += " --user-config=" + os.path.join( emergeUserConfig )
        return options

    def configure( self, defines=""):
        return True

    def make( self ):
        """implements the make step for cmake projects"""
        self.boost = portage.getPackageInstance('win32libs-bin', 'boost-headers')
        self.subinfo.targetInstSrc[ self.subinfo.buildTarget ] = os.path.join(self.boost.sourceDir(),"libs",self.subinfo.targetInstSrc[ self.subinfo.buildTarget ],"build")
        
        self.enterSourceDir()
        cmd  = "bjam"
        cmd += self.configureOptions(self.subinfo.options.configure.defines)
        if utils.verbose() >= 1:
            print(cmd)
        os.system(cmd) and utils.die(
                "command: %s failed" % (cmd))
        return True

    def install( self ):
        """install the target"""
        for root, dirs, files in os.walk( self.buildDir() ):
            for f in files:
                if f.endswith( ".dll" ):
                    utils.copyFile( os.path.join( root, f ),os.path.join( self.imageDir(), "lib", f ) )
                    utils.copyFile( os.path.join( root, f ),os.path.join( self.imageDir(), "bin", f ) )
                elif f.endswith( ".a" ) or f.endswith( ".lib" ):
                    utils.copyFile( os.path.join( root, f ), os.path.join( self.imageDir(), "lib", f ) )
        return True

    def unittest( self ):
        return True


