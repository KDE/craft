import base
import os
import shutil
import utils
from utils import die
import sys
import info

PACKAGE_NAME         = "pcre"
PACKAGE_VER          = "7.5"
PACKAGE_FULL_VER     = "7.5-1"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_VER )
PACKAGE_DLL_NAME     = "pcre"

SRC_URI= """
ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/""" + PACKAGE_FULL_NAME + """.tar.bz2
"""

# fixme: we only need jpeg as dependency!
DEPEND = """
dev-util/win32libs
"""

class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, SRC_URI )
    self.createCombinedPackage = False
    self.instsrcdir = PACKAGE_FULL_NAME
    self.kdeCustomDefines = "-DBUILD_SHARED_LIBS=ON"

  def compile( self ):

    files = """
CMakeLists.txt
config-cmake.h.in
"""
    # we have an own cmake script - copy it to the right place
    src = self.packagedir
    dst = os.path.join( self.workdir, self.instsrcdir )
    for f in files.split():
        shutil.copy( os.path.join( src, f ), os.path.join( dst, f ) )

    return self.kdeCompile()

  def install( self ):
    return self.kdeInstall()

  def make_package( self ):
    # now do packaging with kdewin-packager
    self.doPackaging( PACKAGE_NAME, PACKAGE_FULL_VER, True )

    return True
  
if __name__ == '__main__':
    subclass().execute()
