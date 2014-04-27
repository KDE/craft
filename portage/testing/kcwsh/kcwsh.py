import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kcwsh'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.shortDescription = "a cmd wrapper for konsole"
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['testing/libkcw'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )

