from Package.BinaryPackageBase import *

import os
import shutil
import utils
import info

PACKAGE_NAME         = "libdvdcss"
PACKAGE_VER          = "1.2.10"
PACKAGE_FULL_VER     = "1.2.10"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_VER )
PACKAGE_DLL_NAME     = "libdvdcss"

SRC_URI= """
http://download.videolan.org/pub/libdvdcss/1.2.10/libdvdcss-1.2.10.tar.bz2
"""

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['1.2.10'] = SRC_URI
        self.defaultTarget = '1.2.10'

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
