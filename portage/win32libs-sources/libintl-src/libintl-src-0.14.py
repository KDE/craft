import base
import os
import shutil
import utils

PACKAGE_NAME         = "libintl"
PACKAGE_VER          = "0.14.4"
PACKAGE_FULL_VER     = "0.14.4-2"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_VER )
PACKAGE_DLL_NAME     = "libintl3"

SRC_URI= """
http://surfnet.dl.sourceforge.net/sourceforge/gnuwin32/""" + PACKAGE_FULL_NAME + """-bin.zip
http://surfnet.dl.sourceforge.net/sourceforge/gnuwin32/""" + PACKAGE_FULL_NAME + """-lib.zip
"""

DEPEND = """
"""

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, SRC_URI, args=args )
    self.createCombinedPackage = True

  def compile( self ):
    # binary-only package - nothing to compile
    return True

  def install( self ):
    # that's one of the best packages I've seen from gnuwin32 - nothing to do here :)
    dst = os.path.join( self.imagedir )
    utils.cleanDirectory( dst )
    dst = os.path.join( self.imagedir, self.instdestdir )
    utils.cleanDirectory( dst )

    src = os.path.join( self.workdir, self.instsrcdir )
    utils.copySrcDirToDestDir( src, dst )

    # we better recreate the import libs... :)
    dst = os.path.join( dst, "lib" )
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
