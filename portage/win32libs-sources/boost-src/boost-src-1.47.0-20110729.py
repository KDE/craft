import os
import shutil

import utils
import base
import info

class subinfo(info.infoclass):
    def setTargets(self):
        version = portage.getPackageInstance('win32libs-sources', 'boost-headers-src').subinfo.defaultTarget
        self.targets[version] = ''
        self.defaultTarget = version
        self.shortDescription = "portable C++ libraries"

    def setDependencies(self):
        self.dependencies['win32libs-bin/boost-headers'] = 'default'
        self.dependencies['win32libs-bin/boost-thread'] = 'default'
        self.dependencies['win32libs-bin/boost-system'] = 'default'
        self.dependencies['win32libs-bin/boost-program-options'] = 'default'
        self.dependencies['win32libs-bin/boost-python'] = 'default'
        self.buildDependencies['virtual/base'] = 'default'

from Package.VirtualPackageBase import *

class Package( VirtualPackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        VirtualPackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()

