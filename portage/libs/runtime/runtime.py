import info
from Package.VirtualPackageBase import VirtualPackageBase


class subinfo( info.infoclass ):
    def setTargets( self ):
        # not used  yet only for reference
        self.svnTargets['master'] = ""
        self.shortDescription = "the mingw compiler runtime package"
        self.defaultTarget = 'master'

    def setDependencies( self ):
        self.buildDependencies[ 'virtual/base' ] = 'default'

from Package.BinaryPackageBase import *
import compiler


class PackageMinGW( BinaryPackageBase ):
    def __init__( self ):
        BinaryPackageBase.__init__( self )
        if compiler.isMinGW():
            self.subinfo.options.package.version = compiler.getGCCVersion()

    def fetch(self):
        return True

    def unpack( self ):
        destdir = os.path.join( self.sourceDir(), "bin" )
        utils.createDir( self.sourceDir() )
        utils.createDir( destdir )

        postfix = ""
        if self.buildType() == "Debug":
            postfix = "d"

        srcdir = None
        files = []
        if self.subinfo.options.features.legacyGCC:
            if compiler.isMinGW_W32():
                srcdir = os.path.join( self.rootdir, "mingw", "bin" )
            elif compiler.isMinGW_W64():
                srcdir = os.path.join( self.rootdir, "mingw64", "bin" )
            files = [ 'libgcc_s_sjlj-1.dll', 'libgomp-1.dll' ]
        else:
            files = [ 'libgomp-1.dll', 'libstdc++-6.dll', 'libwinpthread-1.dll' ]
            if compiler.isMinGW_W32():
                files.append('libgcc_s_sjlj-1.dll')
                srcdir = os.path.join( self.rootdir, "mingw", "bin" )
            elif compiler.isMinGW_W64():
                files.append('libgcc_s_seh-1.dll')
                srcdir = os.path.join( self.rootdir, "mingw64", "bin" )

        for file in files:
            utils.copyFile( os.path.join( srcdir, file ), os.path.join( destdir, file ), linkOnly=False )
        return True


if compiler.isMinGW():
    class Package(PackageMinGW):
        def __init__( self ):
            PackageMinGW.__init__( self )
else:
    class Package(VirtualPackageBase):
        pass
