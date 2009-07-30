# -*- coding: utf-8 -*-
import base
import info

SRC_URI= """
http://winkde.org/pub/kde/ports/win32/repository/other/Git-1.6.3-preview20090507-2.tar.bz2
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.6.3'] = SRC_URI
        self.targetInstSrc['1.6.3'] = ""
        self.targetMergePath['1.6.3'] = "git";
        self.defaultTarget = '1.6.3'
   

from Source.ArchiveSource import *
from BuildSystem.BinaryBuildSystem import *
from Package.PackageBase import *

class Package(PackageBase, ArchiveSource, BinaryBuildSystem):
    def __init__( self):
        self.subinfo = subinfo()
        PackageBase.__init__(self)
        ArchiveSource.__init__(self)
        BinaryBuildSystem.__init__(self)
        # no packager required 

if __name__ == '__main__':
    Package().execute()
