import base
import os
import shutil
import utils
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['5.2.1'] = 'http://downloads.sourceforge.net/project/stlport/STLport/STLport-5.2.1/STLport-5.2.1.tar.bz2'
        self.targetInstSrc['5.2.1'] = 'STLport-5.2.1'
        
        self.defaultTarget = '5.2.1'
        
        self.options.package.withCompiler = False

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

from Package.QMakePackageBase import *

class Package(QMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        QMakePackageBase.__init__(self)
        
    def setupEnviroment( self ):
        if self.isTargetBuild():
            self.setupTargetToolchain()
            if self.buildPlatform() == "WM50" or self.buildPlatform() == "WM60" or self.buildPlatform() == "WM65":
                os.putenv("OSVERSION","WCE500")
            
            os.putenv("PLATFORM","Windows CE 6")
            os.putenv("TARGETCPU",self.buildArchitecture())
        
    def configure( self ):
        print "entering %s" % self.sourceDir()
        os.chdir( self.sourceDir() )
        
        self.setupEnviroment()
            
        cmd = "configure "
        if self.compiler() == "mingw" or self.compiler() == "mingw4":
            utils.die("STLPort can not be compiled with mingw.")
        if not self.isTargetBuild():
            if self.compiler() == "msvc2008":
                cmd += "msvc9"
            elif self.compiler() == "msvc2005":
                cmd += "msvc8"
        else:
            if self.compiler() == "msvc2008":
                cmd += "evc9"
            elif self.compiler() == "msvc2005":
                cmd += "evc8"

        print "running: %s" % cmd
        return self.system( cmd )
        

    def make( self ):    
        print "entering %s" % os.path.join(self.sourceDir(), "build", "lib")
        os.chdir( os.path.join(self.sourceDir(), "build", "lib") )
        
        self.setupEnviroment()
        
        self.system( "nmake clean" )
        
        return self.system( "nmake" )

    def install( self ):
        print "entering %s" % os.path.join(self.sourceDir(), "build", "lib")
        os.chdir( os.path.join(self.sourceDir(), "build", "lib") )
        
        self.setupEnviroment()
        
        self.system( "nmake install" )
        
        if not self.isTargetBuild():
            utils.copySrcDirToDestDir( os.path.join( self.sourceDir(), "bin" ) , os.path.join( self.installDir(), "bin" ) )
            utils.copySrcDirToDestDir( os.path.join( self.sourceDir(), "lib" ) , os.path.join( self.installDir(), "lib" ) )        
        else:
            utils.copySrcDirToDestDir( os.path.join( self.sourceDir(), "bin", "evc9-arm" ) , os.path.join( self.installDir(), "bin" ) )
            utils.copySrcDirToDestDir( os.path.join( self.sourceDir(), "lib", "evc9-arm" ) , os.path.join( self.installDir(), "lib" ) )
        utils.copySrcDirToDestDir( os.path.join( self.sourceDir(), "stlport" ) , os.path.join( self.installDir(), "include", "stlport" ) )
        
        return True

if __name__ == '__main__':
    Package().execute()
