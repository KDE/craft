import os
import shutil

import utils
import base
import info
import compiler

class subinfo(info.infoclass):
    def setTargets(self):
        version = portage.getPackageInstance('win32libs-sources', 'boost-headers-src').subinfo.defaultTarget
        self.targets[version] = ''
        self.targetInstSrc[version] = "python"
        
        self.defaultTarget = version
        self.shortDescription = "portable C++ libraries"

    def setDependencies(self):
        self.buildDependencies['win32libs-sources/boost-headers-src'] = 'default'
        self.buildDependencies['win32libs-sources/boost-bjam-src'] = 'default'

from Package.BoostPackageBase import *

class Package(BoostPackageBase):
    def __init__(self, **args):
        self.subinfo = subinfo()
        BoostPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
