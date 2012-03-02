import os
import shutil

import utils

import info

class subinfo(info.infoclass):
    def setTargets(self):
        version = portage.getPackageInstance('win32libs-bin', 'boost-headers').subinfo.defaultTarget
        self.targets[version] = ''
        self.defaultTarget = version
        self.shortDescription = "portable C++ libraries"

    def setDependencies(self):
        self.buildDependencies['win32libs-bin/boost-headers'] = 'default'
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs-bin/boost-graph'] = 'default'
        self.dependencies['win32libs-bin/boost-program-options'] = 'default'
        self.dependencies['win32libs-bin/boost-python'] = 'default'
        self.dependencies['win32libs-bin/boost-regex'] = 'default'
        self.dependencies['win32libs-bin/boost-system'] = 'default'
        self.dependencies['win32libs-bin/boost-thread'] = 'default'

from Package.VirtualPackageBase import *

class Package( VirtualPackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        VirtualPackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()

