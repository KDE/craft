import info
import os
import utils
from Package.BinaryPackageBase import *

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        self.hardDependencies['dev-util/pexports'] = 'default'

    def setTargets( self ):
        ver = "2.6.32-1"
        ver2 = "2.6.32+.win32"
        self.targets[ ver ] = "ftp://ftp.zlatkovic.com/pub/libxml/oldreleases/libxml2-%s.zip" % ver2
        self.targetInstSrc[ ver ] = "libxml2-%s" % ver2
        self.defaultTarget = ver

class Package(BinaryPackageBase):
    def __init__( self ):
        print "1"
        self.subinfo = subinfo()
        BinaryPackageBase.__init__( self )
        # don't use shortcut to unpack into imageDir()
        self.buildSystemType = 'custom'
        # create combined package
        self.subinfo.options.package.withCompiler = None

    def install( self ):
        srcdir = self.sourceDir()
        dstdir = self.installDir()
        print srcdir
        print dstdir
        utils.cleanDirectory( dstdir )

        os.makedirs( os.path.join( dstdir, "lib" ) )
        
        # binaries - can be used from zip package
        utils.copyDir( os.path.join( srcdir, "bin" ),
                       os.path.join( dstdir, "bin" ) )
        # include - can be used from zip package
        utils.copyDir( os.path.join( srcdir, "include" ),
                       os.path.join( dstdir, "include" ) )
        # contrib - readme.txt
        os.makedirs( os.path.join( dstdir, "contrib", self.subinfo.targetSourcePath() ) )
        utils.copyFile( os.path.join( srcdir, "readme.txt" ),
                        os.path.join( dstdir, "contrib", self.subinfo.targetSourcePath(), "readme.txt" ) )

        # auto-create both import libs with the help of pexports
        self.createImportLibs( "libxml2" )

        return True

if __name__ == '__main__':
    Package().execute()
