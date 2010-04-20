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
        self.targets['0.9.8m'] = 'http://www.openssl.org/source/openssl-0.9.8m.tar.gz'
        self.targetInstSrc['0.9.8m'] = 'openssl-0.9.8m'
        self.patchToApply['0.9.8m'] = ('openssl-wince5.patch', 0)
        
        self.defaultTarget = '0.9.8m'
        
        self.options.package.withCompiler = False

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['dev-util/perl'] = 'default'
        if utils.isCrossCompilingEnabled():
            self.hardDependencies['win32libs-sources/wcecompat-src'] = 'default'

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
            outdir = "out32dll"
            if self.isTargetBuild():
                outdir += "_" + self.buildArchitecture()

            shutil.copy( os.path.join( src, outdir, "libeay32.dll" ) , os.path.join( dst, "bin" ) )
            shutil.copy( os.path.join( src, outdir, "ssleay32.dll" ) , os.path.join( dst, "bin" ) )
            shutil.copy( os.path.join( src, outdir, "libeay32.lib" ) , os.path.join( dst, "lib" ) )
            shutil.copy( os.path.join( src, outdir, "ssleay32.lib" ) , os.path.join( dst, "lib" ) )
            utils.copySrcDirToDestDir( os.path.join( src, "include" ) , os.path.join( dst, "include" ) )

        return True

if __name__ == '__main__':
    Package().execute()
