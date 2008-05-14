import base
import os
import shutil
import utils

PACKAGE_NAME         = "expat"
PACKAGE_VER          = "2.0.1"
PACKAGE_FULL_VER     = "2.0.1"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_VER )
PACKAGE_DLL_NAME     = "libexpat"

SRC_URI= """
http://kent.dl.sourceforge.net/sourceforge/expat/expat-win32bin-2.0.1.exe
"""

DEPEND = """
"""

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, SRC_URI, args=args )
    self.createCombinedPackage = True

  def unpack( self ):

    # hopefully only one...
    for filename in self.filenames:
        self.system( os.path.join( self.downloaddir, filename ) + " /DIR=\"" + self.workdir + "\" /SILENT")

    return True

  def compile( self ):
    # binary-only package - nothing to compile
    return True

  def install( self ):
    # cleanup
    dst = os.path.join( self.imagedir )
    utils.cleanDirectory( dst )
    dst = os.path.join( self.imagedir, self.instdestdir )
    utils.cleanDirectory( dst )

    # /bin only contains zlib1.dll
    dst = os.path.join( self.imagedir, self.instdestdir, "bin" )
    utils.cleanDirectory( dst )

    src = os.path.join( self.workdir, self.instsrcdir, "bin", PACKAGE_DLL_NAME + ".dll" )
    dst = os.path.join( self.imagedir, self.instdestdir, "bin", PACKAGE_DLL_NAME + ".dll" )
    shutil.copy( src, dst )

    # /contrib/PACKAGE_NAME/PACKAGE_FULL_VER
    dst = os.path.join( self.imagedir, self.instdestdir, "contrib" )
    utils.cleanDirectory( dst )
    dst = os.path.join( dst, PACKAGE_NAME )
    utils.cleanDirectory( dst )
    dst = os.path.join( dst, PACKAGE_FULL_VER )
    utils.cleanDirectory( dst )

    src = os.path.join( self.workdir )
    shutil.copy( os.path.join( src, "README.txt" ),  os.path.join( dst, "README.txt" ) )

    # /doc can be used from zip package
    src = os.path.join( self.workdir, self.instsrcdir, "doc" )
    dst = os.path.join( self.imagedir, self.instdestdir, "doc" )
    utils.copySrcDirToDestDir( src, dst )

    # /include needs a rebuild... :(
    src = os.path.join( self.workdir, self.instsrcdir, "Source", "lib" )
    dst = os.path.join( self.imagedir, self.instdestdir, "include" )
    utils.cleanDirectory( dst )
    shutil.copy( os.path.join( src, "expat.h" ),  os.path.join( dst, "expat.h" ) )
    shutil.copy( os.path.join( src, "expat_external.h" ),  os.path.join( dst, "expat_external.h" ) )

    # /lib needs a complete rebuild - done in make_package
    dst = os.path.join( self.imagedir, self.instdestdir, "lib" )
    utils.cleanDirectory( dst )

    return True
  def make_package( self ):
    self.instsrcdir = "source"

    # auto-create both import libs with the help of pexports
    self.createImportLibs( PACKAGE_DLL_NAME )

    # now do packaging with kdewin-packager
    self.doPackaging( PACKAGE_NAME, PACKAGE_FULL_VER, True )

    return True
  
if __name__ == '__main__':
    subclass().execute()
