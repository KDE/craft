import info
import utils

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['dev-util/pexports'] = 'default'
        self.hardDependencies['gnuwin32/sed'] = 'default'
        self.hardDependencies['gnuwin32/wget'] = 'default'

    def setTargets( self ):
        self.targets['6b-5'] = 'http://downloads.sourceforge.net/sourceforge/gnuwin32/jpeg-6b-4.exe'
        self.defaultTarget = '6b-5'

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
        os.makedirs( os.path.join( dstdir, "lib" ) )

        # jpeg binaries
        utils.copyFile( os.path.join( srcdir, "Bin", "jpeg62.dll" ),
                        os.path.join( dstdir, "bin", "jpeg.dll") )
        # jpeg include dir
        utils.copyDir( os.path.join( srcdir, "include" ),
                       os.path.join( dstdir, "include" ) )
         # contrib
        utils.copyDir( os.path.join( srcdir, "contrib" ),
                       os.path.join( dstdir, "contrib" ) )
        # auto-create both import libs with the help of pexports
        self.createImportLibs( "jpeg" )
        
        return True

if __name__ == '__main__':
    Package().execute()
