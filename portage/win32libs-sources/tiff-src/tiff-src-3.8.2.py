import base
import os
import shutil
import utils
import info

PACKAGE_NAME         = "tiff"
PACKAGE_VER          = "3.8.2"
PACKAGE_FULL_VER     = "3.8.2-2"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_VER )
PACKAGE_DLL_NAME     = "libtiff3"

SRC_URI= """
http://downloads.sourceforge.net/sourceforge/gnuwin32/tiff-3.8.2-1-bin.zip
http://downloads.sourceforge.net/sourceforge/gnuwin32/tiff-3.8.2-1-lib.zip
"""

DEPEND = """
"""

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['3.8.2'] = SRC_URI
        self.defaultTarget = '3.8.2'
        
class subclass( base.baseclass ):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.createCombinedPackage = True
    self.subinfo = subinfo()

  def install( self ):
    # cleanup
    dst = os.path.join( self.imagedir )
    utils.cleanDirectory( dst )
    dst = os.path.join( self.imagedir, self.instdestdir )
    utils.cleanDirectory( dst )

    # /bin only contains libtiff3.dll
    dst = os.path.join( self.imagedir, self.instdestdir, "bin" )
    utils.cleanDirectory( dst )

    src = os.path.join( self.workdir, self.instsrcdir, "bin", PACKAGE_DLL_NAME + ".dll" )
    dst = os.path.join( self.imagedir, self.instdestdir, "bin", PACKAGE_DLL_NAME + ".dll" )
    shutil.copy( src, dst )

    # /include can be used from zip package
    src = os.path.join( self.workdir, self.instsrcdir, "include" )
    dst = os.path.join( self.imagedir, self.instdestdir, "include" )
    utils.copySrcDirToDestDir( src, dst )
    
    # /contrib too
    src = os.path.join( self.workdir, self.instsrcdir, "contrib" )
    dst = os.path.join( self.imagedir, self.instdestdir, "contrib" )
    utils.copySrcDirToDestDir( src, dst )

    # /man too
    src = os.path.join( self.workdir, self.instsrcdir, "man" )
    dst = os.path.join( self.imagedir, self.instdestdir, "man" )
    utils.copySrcDirToDestDir( src, dst )

    # /lib needs a complete rebuild - done in make_package
    dst = os.path.join( self.imagedir, self.instdestdir, "lib" )
    utils.cleanDirectory( dst )

    return True
  def make_package( self ):
    self.instsrcdir = ""

    # auto-create both import libs with the help of pexports
    self.createImportLibs( PACKAGE_DLL_NAME )

    # now do packaging with kdewin-packager
    self.doPackaging( PACKAGE_NAME, PACKAGE_FULL_VER, False )

    return True
  
if __name__ == '__main__':
    subclass().execute()
