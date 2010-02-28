import info
import utils

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['dev-util/pexports'] = 'default'
        self.hardDependencies['gnuwin32/sed'] = 'default'
        self.hardDependencies['gnuwin32/wget'] = 'default'

    def setTargets( self ):
        self.targets['2.0.1'] = 'http://downloads.sourceforge.net/sourceforge/expat/expat-win32bin-2.0.1.exe'
        self.defaultTarget = '2.0.1'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__( self )
        # don't use shortcut to unpack into imageDir()
        self.buildSystemType = 'custom'
        # create combined package
        self.subinfo.options.package.withCompiler = None

    def unpack( self ):
  
        # hopefully only one...
        for filename in self.localFileNames():
            self.system( os.path.join( self.downloadDir(), filename ) + " /DIR=\"" + self.workDir() + "\" /SILENT")
        return True

    def install( self ):
        srcdir = self.sourceDir()
        dstdir = self.installDir()

        utils.cleanDirectory( dstdir )
        os.makedirs( os.path.join( dstdir, "bin" ) )
        os.makedirs( os.path.join( dstdir, "include" ) )
        os.makedirs( os.path.join( dstdir, "lib" ) )

        # expat binaries
        utils.copyFile( os.path.join( srcdir, "Bin", "libexpat.dll" ),
                        os.path.join( dstdir, "bin", "libexpat.dll") )
        # doc can be used from zip package
        utils.copyDir( os.path.join( srcdir, "doc" ),
                       os.path.join( dstdir, "doc", self.package + "-" + self.subinfo.buildTarget ) )
        # expat include dir
        for f in ( "expat.h", "expat_external.h" ):
          utils.copyFile( os.path.join( srcdir, "Source", "lib", f ),
                          os.path.join( dstdir, "include", f ) )
        # contrib
        os.makedirs( os.path.join( dstdir, "contrib", self.package + "-" + self.subinfo.buildTarget ) )
        utils.copyFile( os.path.join( srcdir, "README.txt" ),
                        os.path.join( dstdir, "contrib", self.package + "-" + self.subinfo.buildTarget, "README.txt" ) )
        # auto-create both import libs with the help of pexports
        self.createImportLibs( "libexpat" )
        
        return True

if __name__ == '__main__':
    Package().execute()
