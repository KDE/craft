import info
import os
import utils

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.7.7'] = "ftp://xmlsoft.org/libxml2/libxml2-sources-2.7.7.tar.gz"
        self.targetInstSrc['2.7.7'] = 'libxml2-2.7.7'
        self.defaultTarget = '2.7.7'
        
        if self.hasTargetPlatform():
            self.patchToApply['2.7.7'] = ('libxml2-2.7.7-wince5.patch', 0)

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        
    def unpack(self):
        CMakePackageBase.unpack(self)
        src = os.path.join( os.path.join( self.sourceDir(), "win32" ), "wince" )
        utils.copyFile( os.path.join( src, "wincecompat.h" ), os.path.join(self.sourceDir(), "wincecompat.h") )
        utils.copyFile( os.path.join( src, "wincecompat.c" ), os.path.join(self.sourceDir(), "wincecompat.c") )
        return True

    def configure(self):
        os.chdir( os.path.join( self.sourceDir(), "win32" ) )

        if self.buildType() == "Debug":
            cruntime="/MDd"
            dbg="yes"
        else:
            cruntime="/MD"
            dbg="no"

        if "msvc" in self.compiler():
            compiler="msvc"
        else:
            compiler="mingw"

        command =  r"cscript configure.js compiler=%s cruntime=%s vcmanifest=yes " % (compiler,cruntime)
        command += r"prefix=%s sodir=$(PREFIX)\bin " % self.installDir()
        command += r"debug=%s threads=no iconv=no xml_debug=no ftp=no http=no" % dbg
        
        return self.system( command )
        
    def make(self):
        os.chdir( os.path.join( self.sourceDir(), "win32" ) )
        
        if self.hasTargetPlatform():
            self.setupCrossToolchain()

        return self.system( "nmake /f Makefile.msvc rebuild" )
        
    def install(self):
        os.chdir( os.path.join( self.sourceDir(), "win32" ) )
        return self.system( "nmake /f Makefile.msvc install" )


if __name__ == '__main__':
    Package().execute()
