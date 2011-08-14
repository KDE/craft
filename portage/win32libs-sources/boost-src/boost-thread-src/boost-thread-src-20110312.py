import os
import shutil

import utils
import base
import info
import compiler

class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['1.44.0'] = ''
        self.targetInstSrc['1.44.0'] = "thread"
        
        self.defaultTarget = '1.44.0'
        self.shortDescription = "portable C++ libraries"

    def setDependencies(self):
        self.buildDependencies['dev-util/bjam'] = 'default'
        self.buildDependencies['win32libs-sources/boost-src'] = 'default'

from Package.BoostPackageBase import *

class Package(BoostPackageBase):
    def __init__(self, **args):
        self.subinfo = subinfo()
        BoostPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
