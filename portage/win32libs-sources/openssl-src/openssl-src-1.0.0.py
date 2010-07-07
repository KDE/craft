import base
import os
import shutil
import utils
import info
import platform
import compiler

class subinfo(info.infoclass):
    def setTargets( self ):   
        for ver in [ '0.9.8k' , '0.9.8m' ,'1.0.0' , '1.0.0a']:
            self.targets[ver] = 'http://www.openssl.org/source/openssl-'+ver+'.tar.gz'
            self.targetInstSrc[ver] = 'openssl-'+ver
            if compiler.isMSVC():
              self.patchToApply[ver] = ('openssl-'+ver+'.diff', 1)
            self.targetDigestUrls[ver] = 'http://www.openssl.org/source/openssl-'+ver+'.tar.gz.sha1'
            
        if compiler.isMinGW():
            self.defaultTarget = '1.0.0a'
        else:
            self.defaultTarget = '1.0.0'
        
        self.options.package.withCompiler = False

    def setDependencies( self ):
            self.hardDependencies['virtual/base'] = 'default'
            self.hardDependencies['dev-util/perl'] = 'default'
            if platform.isCrossCompilingEnabled():
                self.hardDependencies['win32libs-sources/wcecompat-src'] = 'default'
            if compiler.isMinGW():
                self.hardDependencies['dev-util/msys'] = 'default'
                self.hardDependencies['win32libs-bin/zlib'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = False


from Package.CMakePackageBase import *

class PackageCMake(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

    def compile( self ):       
        os.chdir( self.sourceDir() )
        cmd = ""
        if self.isTargetBuild():
            """WinCE cross-building environment setup"""
            config = "VC-CE"
            os.environ["WCECOMPAT"] = self.mergeDestinationDir()
            os.environ["TARGETCPU"] = self.buildArchitecture() 
            os.environ["PLATFORM"] = self.buildPlatform()
            if self.buildPlatform() == "WM50":
                os.environ["OSVERSION"] = "WCE501"
            elif self.buildPlatform() == "WM60" or self.buildPlatform() == "WM65":
                os.environ["OSVERSION"] = "WCE502"
        else:
            config = "VC-WIN32"

        if not self.system( "perl Configure %s" % config, "configure" ):
            return False

        if not self.system( "ms\do_ms.bat", "configure" ):
            return False
            
        if self.isTargetBuild():
            self.setupTargetToolchain()
            # Set the include path for the wcecompat files (e.g. errno.h). Setting it through
            # the Configure script generates errors due to the the backslashes in the path
            wcecompatincdir = os.path.join( os.path.join( self.mergeDestinationDir(), "include" ), "wcecompat" )
            os.putenv( "INCLUDE", wcecompatincdir + ";" + os.getenv("INCLUDE") )
            cmd = r"nmake -f ms\cedll.mak"
        else:
            cmd = r"nmake -f ms\ntdll.mak"

        return self.system( cmd )

    def install( self ):        
        src = self.sourceDir()
        dst = self.imageDir()

        if not os.path.isdir( dst ):
            os.mkdir( dst )
        if not os.path.isdir( os.path.join( dst, "bin" ) ):
            os.mkdir( os.path.join( dst, "bin" ) )
        if not os.path.isdir( os.path.join( dst, "lib" ) ):
            os.mkdir( os.path.join( dst, "lib" ) )
        if not os.path.isdir( os.path.join( dst, "include" ) ):
            os.mkdir( os.path.join( dst, "include" ) )

        outdir = "out32dll"
        if self.isTargetBuild():
            outdir += "_" + self.buildArchitecture()

        shutil.copy( os.path.join( src, outdir, "libeay32.dll" ) , os.path.join( dst, "bin" ) )
        shutil.copy( os.path.join( src, outdir, "ssleay32.dll" ) , os.path.join( dst, "bin" ) )
        shutil.copy( os.path.join( src, outdir, "libeay32.lib" ) , os.path.join( dst, "lib" ) )
        shutil.copy( os.path.join( src, outdir, "ssleay32.lib" ) , os.path.join( dst, "lib" ) )
        utils.copySrcDirToDestDir( os.path.join( src, "include" ) , os.path.join( dst, "include" ) )
        
        return True
        
        
from Package.PackageBase import *
from Source.MultiSource import *
from BuildSystem.AutoToolsBuildSystem import *
from Packager.KDEWinPackager import *;

class PackageMSys(PackageBase, MultiSource, AutoToolsBuildSystem, KDEWinPackager):
    def __init__( self ):
        self.subinfo = subinfo()
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        AutoToolsBuildSystem.__init__(self)
        KDEWinPackager.__init__(self)
        self.subinfo.options.package.packageName = 'openssl'
        self.subinfo.options.package.withCompiler = False
        self.subinfo.options.package.packSources = False
        self.subinfo.options.install.useDestDir = False
        self.shell = MSysShell()
        
        self.buildInSource=True

        # target install needs perl with native path on configure time
        self.subinfo.options.configure.defines = " shared enable-md2 zlib-dynamic --with-zlib-lib=libzlib.dll.a --with-zlib-include=%s %s" % (
            MSysShell().toNativePath(os.path.join( self.mergeDestinationDir() ,"include" )) ,compiler.getSimpleCompilerName() )
        if compiler.isMinGW32() and not compiler.isMinGW_W32():
            self.subinfo.options.configure.defines += " -DOPENSSL_NO_CAPIENG"
           
      
    def install (self):
      self.enterSourceDir()       
      self.shell.execute(self.sourceDir(), self.makeProgram, "install_sw" )
      self.shell.execute(os.path.join( self.imageDir() , "lib"), "chmod" ,"664 *")
      self.shell.execute(os.path.join( self.imageDir() , "lib" , "engines" ), "chmod" , "755 *")
      shutil.move( os.path.join( self.imageDir(),  "lib" , "libcrypto.dll.a" ) , os.path.join( self.imageDir() , "lib" , "libeay32.dll.a" ) )
      shutil.move( os.path.join( self.imageDir(), "lib" , "libssl.dll.a" ) , os.path.join( self.imageDir() , "lib" , "ssleay32.dll.a" ) )
      return True
      
      

if compiler.isMinGW():
    class Package(PackageMSys):
        def __init__( self ):
            PackageMSys.__init__( self )
else:
    class Package(PackageCMake):
        def __init__( self ):
            PackageCMake.__init__( self )
            
if __name__ == '__main__':
      Package().execute()

