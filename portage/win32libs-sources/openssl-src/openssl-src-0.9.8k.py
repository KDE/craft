import base
import os
import shutil
import utils
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.9.8k'] = 'http://www.openssl.org/source/openssl-0.9.8k.tar.gz'
        self.targetInstSrc['0.9.8k'] = 'openssl-0.9.8k'
        self.patchToApply['0.9.8k'] = ('openssl-0.9.8k.diff', 1)
        self.targets['1.0.0'] = 'http://www.openssl.org/source/openssl-1.0.0.tar.gz'
        self.targetInstSrc['1.0.0'] = 'openssl-1.0.0'
        self.patchToApply['1.0.0'] = ('openssl-1.0.0-20100402.diff', 1)
        self.options.package.withCompiler = False
        self.defaultTarget = '0.9.8k'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['dev-util/perl'] = 'default'
        
from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

    def compile( self ):
        os.chdir( self.sourceDir() )
        cmd = ""
        if self.compiler() == "mingw" or self.compiler() == "mingw4":
            cmd = "ms\mingw32.bat"
        else:
            cmd = "ms\\32all.bat"
      
        return self.system( cmd )

    def install( self ):
        src = self.sourceDir()
        dst = self.imageDir()

        if not os.path.isdir( dst ):
            os.mkdir( dst )
            os.mkdir( os.path.join( dst, "bin" ) )
            os.mkdir( os.path.join( dst, "lib" ) )
            os.mkdir( os.path.join( dst, "include" ) )

        if self.compiler() == "mingw" or self.compiler() == "mingw4":
            shutil.copy( os.path.join( src, "libeay32.dll" ) , os.path.join( dst, "bin" ) )
            shutil.copy( os.path.join( src, "libssl32.dll" ) , os.path.join( dst, "bin", "ssleay32.dll" ) )
            utils.copySrcDirToDestDir( os.path.join( src, "outinc" ) , os.path.join( dst, "include" ) )
            shutil.copy( os.path.join( src, "ms", "applink.c" ) , os.path.join( dst, "include", "openssl" ) )

            # auto-create both import libs with the help of pexports
            for f in "libeay32 ssleay32".split():
                self.stripLibs( f )
                self.createImportLibs( f )

        else:
            shutil.copy( os.path.join( src, "out32dll", "libeay32.dll" ) , os.path.join( dst, "bin" ) )
            shutil.copy( os.path.join( src, "out32dll", "ssleay32.dll" ) , os.path.join( dst, "bin" ) )
            shutil.copy( os.path.join( src, "out32dll", "libeay32.lib" ) , os.path.join( dst, "lib" ) )
            shutil.copy( os.path.join( src, "out32dll", "ssleay32.lib" ) , os.path.join( dst, "lib" ) )
            utils.copySrcDirToDestDir( os.path.join( src, "include" ) , os.path.join( dst, "include" ) )

        return True

if __name__ == '__main__':
    Package().execute()
