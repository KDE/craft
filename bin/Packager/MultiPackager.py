# 
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

from KDEWinPackager import *;
from CPackPackager import *;
from MSInstallerPackager import *;
from InnoSetupPackager import *;

import info
import utils

class MultiPackager():
    def __init__(self,packagerType=None):
        utils.debug( "MultiPackager __init__ %s" %packagerType, 2 )
        self.packager = None
        if packagerType == 'KDEWin' or packagerType == 'kdewin' or packagerType == None:
            self.packager = KDEWinPackager()
        elif packagerType == 'CPack':
            self.packager = CPackPackager()
        elif packagerType == 'Inno' or packagerType == 'inno':
            self.packager = InnoSetupPackager()
        else:
            utils.die("none or unsupported packager set, use self.packagerType='type', where type could be 'KDEWin'")

        self.packager.subinfo = self.subinfo
        self.packager.parent = self
        self.packager.category = self.category
        self.packager.package = self.package
        self.packager.version = self.version
        self.packager.buildTarget = self.subinfo.buildTarget
        self.packager.PV = self.PV

    def createPackage(self):
        return self.packager.createPackage()
        
    def make_package(self):
        return self.packager.createPackage()
