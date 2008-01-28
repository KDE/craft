import base
import os
import shutil
import utils
from utils import die
import sys
import info

PACKAGE_NAME         = "pcre"
PACKAGE_VER          = "7.6"
PACKAGE_FULL_VER     = "7.6-1"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_VER )
PACKAGE_DLL_NAME     = "pcre"

SRC_URI= """
ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/""" + PACKAGE_FULL_NAME + """.tar.bz2
"""

# fixme: we only need jpeg as dependency!
DEPEND = """
dev-util/win32libs
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets[PACKAGE_VER] = SRC_URI
        self.defaultTarget = PACKAGE_VER

class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, SRC_URI )
    self.createCombinedPackage = False
    self.subinfo = subinfo()
    self.instsrcdir = PACKAGE_FULL_NAME
    self.kdeCustomDefines += "-DBUILD_SHARED_LIBS=ON "
    self.kdeCustomDefines += "-DPCRE_SUPPORT_UNICODE_PROPERTIES=ON "
    self.kdeCustomDefines += "-DPCRE_SUPPORT_UTF8=ON "
    self.kdeCustomDefines += "-DPCRE_EBCDIC=ON "

  def compile( self ):
    return self.kdeCompile()

  def install( self ):
    return self.kdeInstall()

  def make_package( self ):
    # now do packaging with kdewin-packager
    self.doPackaging( PACKAGE_NAME, PACKAGE_FULL_VER, True )

    return True
  
if __name__ == '__main__':
    subclass().execute()
