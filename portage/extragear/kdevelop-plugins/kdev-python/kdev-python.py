import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kdev-python|frameworks|'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.shortDescription = "python support for kdevelop"
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['extragear/kdevplatform'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )

