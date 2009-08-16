# -*- coding: iso-8859-15 -*-
import base
import info
import os
import shutil
import utils

PACKAGE_NAME         = "boost-jam"
PACKAGE_VER          = "3.1.16"
PACKAGE_FULL_VER     = "3.1.16-1"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_FULL_VER)

SRC_URI= """
http://downloads.sourceforge.net/boost/""" + PACKAGE_FULL_NAME + """-ntx86.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['3.1.16-1'] = SRC_URI
        self.targetInstSrc['3.1.16-1'] = PACKAGE_FULL_NAME + "-ntx86"
        self.defaultTarget = '3.1.16-1'
        self.targetMergeSourcePath['3.1.16-1'] = "boost-jam-3.1.16-1-ntx86"
        self.targetMergePath['3.1.16-1'] = "dev-utils/bin";


    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        BinaryPackageBase.__init__(self)
    
    def unpack(self):
        if not BinaryPackageBase.unpack(self):
            return False
        ## \todo rename directory "boost-jam-3.1.16-1-ntx86" to "bin"
        return True

if __name__ == '__main__':
    Package().execute()
