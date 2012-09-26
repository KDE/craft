import os
import shutil
import utils
import info
import emergePlatform
import compiler

class subinfo( info.infoclass ):

    def setTargets( self ):
        self.targets[ '3.1.1' ] = 'http://mirror.netcologne.de/apache.org//xerces/c/3/sources/xerces-c-3.1.1.tar.gz'
        self.targetInstSrc[ '3.1.1' ] = 'xerces-c-3.1.1'
        #self.patchToApply['3.1.1'] = ('xerces-c-3.1.1.diff', 1)
        self.targetDigests['3.1.1'] = '177ec838c5119df57ec77eddec9a29f7e754c8b2'

        self.shortDescription = "The Xerces C++ library" 
        self.defaultTarget = '3.1.1'

    def setDependencies( self ):
            self.buildDependencies['virtual/base'] = 'default'
            if compiler.isMinGW():
                self.buildDependencies['dev-util/msys'] = 'default'

from Package.CMakePackageBase import *

class PackageCMake(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

    def compile( self ):
        os.chdir( self.sourceDir() )
        cmd = "msbuild /target:XercesLib"
        if self.buildType() == "Debug":
            cmd += " /p:Configuration=Debug"
        else:
            cmd += " /p:Configuration=Release"
        cmd += " projects\\Win32\\VC10\\xerces-all\\xerces-all.sln"

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
        if not os.path.isdir( os.path.join( dst, "include", "xercesc" ) ):
            os.mkdir( os.path.join( dst, "include", "xercesc" ) )

        outdir = "Build\\Win32\\VC10\\"

        if self.buildType() == "Debug":
            outdir += "Debug"
            outdll = "xerces-c_3_1D.dll"
            outimplib = "xerces-c_3D.lib"
        else:
            outdir += "Release"
            outdll = "xerces-c_3_1.dll"
            outimplib = "xerces-c_3.lib"

        shutil.copy( os.path.join( src, outdir, outdll ) , os.path.join( dst, "bin" ) )
        shutil.copy( os.path.join( src, outdir, outimplib ) , os.path.join( dst, "lib" ) )
        # include directory:
        destsubdir = os.path.join( dst, "include", "xercesc" )
        utils.copySrcDirToDestDir( os.path.join( src, "src", "xercesc" ), destsubdir )
        shutil.rmtree( os.path.join( destsubdir, "NLS" ) )
        shutil.rmtree( os.path.join( destsubdir, "util", "MsgLoaders", "ICU" ) )
        shutil.rmtree( os.path.join( destsubdir, "util", "MsgLoaders", "InMemory" ) )
        shutil.rmtree( os.path.join( destsubdir, "util", "MsgLoaders", "MsgCatalog" ) )
        shutil.rmtree( os.path.join( destsubdir, "util", "NetAccessors", "Curl" ) )
        shutil.rmtree( os.path.join( destsubdir, "util", "NetAccessors", "MacOSURLAccessCF" ) )
        shutil.rmtree( os.path.join( destsubdir, "util", "NetAccessors", "Socket" ) )
        shutil.rmtree( os.path.join( destsubdir, "util", "Transcoders", "Iconv" ) )
        shutil.rmtree( os.path.join( destsubdir, "util", "Transcoders", "IconvGNU" ) )
        shutil.rmtree( os.path.join( destsubdir, "util", "Transcoders", "ICU" ) )
        shutil.rmtree( os.path.join( destsubdir, "util", "Transcoders", "MacOSUnicodeConverter" ) )
        os.remove( os.path.join( destsubdir, "util", "Xerces_autoconf_config.borland.hpp" ) )
        os.remove( os.path.join( destsubdir, "util", "Xerces_autoconf_config.hpp.in" ) )
        os.remove( os.path.join( destsubdir, "util", "Xerces_autoconf_config.hpp" ) )
        os.remove( os.path.join( destsubdir, "util", "FileManagers", "PosixFileMgr.hpp" ) )
        os.remove( os.path.join( destsubdir, "util", "MsgLoaders", "Win32", "Version.rc" ) )
        os.remove( os.path.join( destsubdir, "util", "MutexManagers", "NoThreadMutexMgr.hpp" ) )
        os.remove( os.path.join( destsubdir, "util", "MutexManagers", "PosixMutexMgr.hpp" ) )
        for root, _, files in os.walk( destsubdir ):
            for fileName in files:
                if fileName.endswith( ".cpp" ): os.remove( os.path.join( root, fileName ) )
        # now in the end copy config fileName
        os.rename( os.path.join( destsubdir, "util", "Xerces_autoconf_config.msvc.hpp" ), os.path.join( destsubdir, "util", "Xerces_autoconf_config.hpp" ) )
        return True


from Package.AutoToolsPackageBase import *

class PackageMSys(AutoToolsPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        self.subinfo.options.package.packSources = False
        AutoToolsPackageBase.__init__(self)
        self.shell = MSysShell()
        self.subinfo.options.configure.defines = "--enable-transcoder-windows --enable-netaccessor-winsock --enable-shared --disable-static"
        self.buildInSource=True

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

