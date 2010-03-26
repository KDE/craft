import base
import os
import shutil
import utils

PACKAGE_NAME         = "mingw-runtime"
PACKAGE_VER          = "3.13"
PACKAGE_FULL_VER     = "3.13"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_VER )
PACKAGE_DLL_NAME     = "libintl3"

SRC_URI= """
http://downloads.sourceforge.net/sourceforge/mingw/""" + PACKAGE_FULL_NAME + """.tar.gz
"""

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, SRC_URI, args=args )

  def compile( self ):
    # binary-only package - nothing to compile
    return True

  def install( self ):
    dst = os.path.join( self.imagedir )
    utils.cleanDirectory( dst )
    dst = os.path.join( self.imagedir, self.instdestdir )
    utils.cleanDirectory( dst )

    src = os.path.join( self.workdir, self.instsrcdir )
    utils.copySrcDirToDestDir( src, dst )

    return True

  def make_package( self ):
    self.instsrcdir = ""

    # now do packaging with kdewin-packager
    self.doPackaging( PACKAGE_NAME, PACKAGE_FULL_VER, False )

    return True
  
if __name__ == '__main__':
    subclass().execute()
