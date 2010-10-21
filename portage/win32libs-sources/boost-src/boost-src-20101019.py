import os
import shutil

import utils
import base
import info
import compiler

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.44.0'] = 'http://downloads.sourceforge.net/boost/boost_1_44_0.7z'
        self.targetDigests['1.44.0'] = '687fb91c328e7292ca4c400dcbd461710d967199'
        self.targetInstSrc['1.44.0'] = 'boost_1_44_0'
        self.defaultTarget = '1.44.0'
    
    def setDependencies( self ):
        self.hardDependencies['dev-util/bjam'] = 'default'
        

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

        self.subinfo.options.configure.defines = " --build-type=minimal " 
        self.subinfo.options.configure.defines += " --build-dir=" + self.buildDir()
        self.subinfo.options.configure.defines += " --prefix=" + self.imageDir()
        self.subinfo.options.configure.defines += " --stagedir=" + os.path.join(self.buildDir(),"stage")
        self.subinfo.options.configure.defines += " link=shared"
        self.subinfo.options.configure.defines += " runtime-link=shared"
        self.subinfo.options.configure.defines += " threading=multi"
        self.subinfo.options.configure.defines += " variant="
        if self.buildType() == "Debug":
            self.subinfo.options.configure.defines += "debug"
        else:
            self.subinfo.options.configure.defines += "release"
        self.subinfo.options.configure.defines += " toolset="
        if compiler.isMinGW():
            self.subinfo.options.configure.defines += "gcc"
        else:
            self.subinfo.options.configure.defines += "msvc"        
        self.subinfo.options.configure.defines += " --with-python --with-program_options"
  
        
    def configure( self ):
        return True

    def install( self ):
        self.enterSourceDir()
        cmd  = "bjam install"
        cmd += self.subinfo.options.configure.defines
        if utils.verbose() >= 1:
            print cmd
        os.system( cmd ) and utils.die( "compile failed because of this cobbled stuff: %s" % ( cmd ) )
        shutil.copytree( os.path.join(self.imageDir(),"lib") , os.path.join(self.imageDir(),"bin")  ,  ignore=shutil.ignore_patterns('*.a','*.lib') )
        shutil.move(os.path.join(self.imageDir(),"include","boost-1_44","boost"),os.path.join(self.imageDir(),"include","boost"))
        shutil.rmtree(os.path.join(self.imageDir(),"include","boost-1_44"))
        return True
        
    def runTest( self ):
        return False
        
        
    def make( self ):
        self.enterSourceDir()
        cmd  = "bjam stage"
        cmd += self.subinfo.options.configure.defines
        if utils.verbose() >= 1:
            print cmd
        os.system( cmd ) and utils.die( "compile failed because of this cobbled stuff: %s" % ( cmd ) )
        return True


if __name__ == '__main__':
    Package().execute()