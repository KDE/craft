# -*- coding: utf-8 -*-
import utils
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://github.com/mauricek/wcecompat.git'
        self.patchToApply['gitHEAD'] = ('wcecompat-wince5.patch', 0)
        self.defaultTarget = 'gitHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['dev-util/perl'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = True
        self.disableTargetBuild = False

from Package.CMakePackageBase import *
                
class TestPackage(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

    def unpack(self):
        # FIXME : find a way to do something like svn export or make out-of-source builds work
        # Currently the emerge fails to clean the build dir due to a .git file which can't be deleted
        # (filename too long probably), which means only the first build succeeds
        CMakePackageBase.unpack( self )
        utils.copySrcDirToDestDir(self.sourceDir(), self.buildDir())
        return True
        
    def configure(self):
        self.enterBuildDir()

        os.environ["TARGETCPU"] = self.buildArchitecture()
        if self.buildPlatform() == "WM50":
            os.environ["OSVERSION"] = "WCE501"
        elif self.buildPlatform() == "WM60" or self.buildPlatform() == "WM65":
            os.environ["OSVERSION"] = "WCE502"

        command = "perl config.pl"
        return self.system( command )

    def make(self):
        self.enterBuildDir()
        self.setupTargetToolchain()
        return self.system( self.makeProgramm ) 

    def install(self):
        src = self.buildDir()
        dst = self.imageDir()

        if not os.path.isdir( dst ):
            os.mkdir( dst )
            os.mkdir( os.path.join( dst, "lib" ) )
            os.mkdir( os.path.join( dst, "include" ) )

        utils.copySrcDirToDestDir( os.path.join( src, "include" ) , os.path.join( os.path.join( dst, "include" ), "wcecompat" ) )
        shutil.copy( os.path.join( src, "lib", "wcecompat.lib" ) , os.path.join( dst, "lib" ) )
        shutil.copy( os.path.join( src, "lib", "wcecompatex.lib" ) , os.path.join( dst, "lib" ) )
        
        return True
    
if __name__ == '__main__':
    TestPackage().execute()
