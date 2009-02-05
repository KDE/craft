import base
import os
import utils
import info
import shutil

class subinfo(info.infoclass):
    def setTargets( self ):
        """ """
        self.targets['0.8.0'] = "http://www.nih.at/libzip/libzip-0.8.tar.gz"
        self.targetInstSrc['0.8.0'] = "libzip-0.8"
        self.defaultTarget = '0.8.0'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()
        self.createCombinedPackage = True
        
    def unpack( self ):
        base.baseclass.unpack( self )
        srcdir = os.path.join( self.packagedir, "zip_err_str.c" )
        destdir = os.path.join( self.workdir, "libzip-0.8", "lib" )
        utils.copySrcDirToDestDir( srcdir, destdir )
        os.chdir( self.workdir )
        self.system( "cd %s && patch -p0 < %s" % ( self.workdir, os.path.join( self.packagedir, "libzip.diff" ) ) )
        return True
        

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()
    
    def make_package( self ):
        self.instsrcdir = ""

        # auto-create both import libs with the help of pexports
        self.createImportLibs( "libzip" )

        # now do packaging with kdewin-packager
        self.doPackaging( "libzip", "0.8.0", True )

        return True
  
if __name__ == '__main__':
    subclass().execute()
