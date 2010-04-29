import os
from shells import MSysShell
import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.0.0'] = 'http://www.openssl.org/source/openssl-1.0.0.tar.gz'
        self.targetDigestUrls['1.0.0'] = 'http://www.openssl.org/source/openssl-1.0.0.tar.gz.sha1'
        self.targetInstSrc['1.0.0'] = "openssl-1.0.0"
        self.patchToApply['1.0.0'] = ('openssl-1.0.0.diff',1)
        
        
        self.defaultTarget = '1.0.0'

    def setDependencies( self ):
        self.hardDependencies['dev-util/msys'] = 'default'
        self.hardDependencies['dev-util/perl'] = 'default'
        self.hardDependencies['win32libs-bin/zlib'] = 'default'

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
        self.subinfo.options.package.packageName = 'openssl'
        self.subinfo.options.package.withCompiler = False
        self.subinfo.options.package.packSources = False
        self.shell = MSysShell()
        
        self.buildInSource=True
        compiler = self.compiler()
        if self.buildArchitecture()=="x64" and compiler == "mingw4":
            compiler="mingw64"
        elif(compiler == "mingw4"):
            compiler="mingw"
        else:
            utils.die("msvc is not supported");

        # target install needs perl with native path on configure time
        os.putenv("PERL",MSysShell().toNativePath(os.path.join( os.environ.get( "KDEROOT" ) , "dev-utils" , "bin" , "perl.exe" )))
        self.subinfo.options.configure.defines = " shared enable-md2 zlib-dynamic --with-zlib-lib=libzlib.dll.a --with-zlib-include=%s %s" % (MSysShell().toNativePath(os.path.join( self.mergeDestinationDir() ,"include" )) ,compiler )
           
      
    def install (self):
      if(not AutoToolsBuildSystem.install(self)):
	return False
      self.shell.execute(os.path.join( self.imageDir() , "lib"), "chmod" ,"664 *")
      self.shell.execute(os.path.join( self.imageDir() , "lib" , "engines" ), "chmod" , "755 *")
      shutil.move( os.path.join( self.imageDir(),  "lib" , "libcrypto.dll.a" ) , os.path.join( self.imageDir() , "lib" , "libeay32.dll.a" ) )
      shutil.move( os.path.join( self.imageDir(), "lib" , "libssl.dll.a" ) , os.path.join( self.imageDir() , "lib" , "ssleay32.dll.a" ) )
      return True
if __name__ == '__main__':
     Package().execute()
