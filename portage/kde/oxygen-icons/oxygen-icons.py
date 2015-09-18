import info
from EmergeConfig import *

class subinfo(info.infoclass):

    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:oxygen-icons'
        self.defaultTarget = 'gitHEAD'
        self.shortDescription = "icons and bitmaps for the oxygen style"

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


