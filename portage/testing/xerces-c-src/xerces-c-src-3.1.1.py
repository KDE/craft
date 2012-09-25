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
#        utils.copySrcDirToDestDir( os.path.join( src, "include" ) , os.path.join( dst, "include" ) )

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

