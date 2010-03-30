import os
from shells import MSysShell
import info


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['dev-util/msys'] = 'default'
        self.hardDependencies['dev-util/perl'] = 'default'
        self.hardDependencies['win32libs-bin/zlib'] = 'default'

    def setTargets( self ):
        self.targets['1.0.0'] = 'http://www.openssl.org/source/openssl-1.0.0.tar.gz'
     
        
        self.targetInstSrc['1.0.0'] = "openssl-1.0.0"
       

        self.defaultTarget = '1.0.0'

from Package.PackageBase import *
from Source.MultiSource import *
from BuildSystem.AutoToolsBuildSystem import *
from Packager.KDEWinPackager import *;

class Package( PackageBase, MultiSource, AutoToolsBuildSystem, KDEWinPackager):
    def __init__( self ):
        self.subinfo = subinfo()
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        AutoToolsBuildSystem.__init__(self)
        KDEWinPackager.__init__(self)
        self.buildInSource=True
        if(self.compiler() == "mingw4"):
          compiler="mingw"
          if( os.getenv("EMERGE_ARCHITECTURE")=="x64"):
            compiler="mingw64"
        else:
            print("msvc is not supported");
        os.putenv("PERL",MSysShell().toNativePath(os.path.join( os.environ.get( "KDEROOT" ) , "dev-utils" , "bin" , "perl.exe" )))
        self.subinfo.options.configure.defines = " shared -enable-md2  zlib-dynamic --with-zlib-lib=libzlib.dll.a --with-zlib-include=%s %s" % (MSysShell().toNativePath(os.path.join( os.environ.get( "KDEROOT" ) ,"include" )) ,compiler )
           
if __name__ == '__main__':
     Package().execute()
