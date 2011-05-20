import utils
import os
import info
import emergePlatform
import compiler

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.6.16'] = ("http://subversion.tigris.org/downloads/subversion-1.6.16.zip "
                                  "http://subversion.tigris.org/downloads/subversion-deps-1.6.16.zip")
        self.defaultTarget = '1.6.16'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['gnuwin32/gawk'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.staticBuild = False


if __name__ == '__main__':
    Package().execute()
