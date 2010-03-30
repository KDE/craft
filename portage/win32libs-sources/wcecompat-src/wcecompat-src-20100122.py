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

from Package.BinaryPackageBase import *
                
class TestPackage(BinaryPackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__( self )

    def unpack(self):
        BinaryPackageBase.unpack(self)
        utils.copySrcDirToDestDir(self.sourceDir(), self.buildDir())
        self.enterBuildDir()

        os.environ["TARGETCPU"] = self.targetArchitecture()
        if self.targetPlatform() == "WM50":
            os.environ["OSVERSION"] = "WCE501"
        elif self.targetPlatform() == "WM60" or self.targetPlatform() == "WM65":
            os.environ["OSVERSION"] = "WCE502"

        command = "perl config.pl"
        return self.system( command )

    def make(self):
        self.enterBuildDir()
        self.setupCrossToolchain()
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
