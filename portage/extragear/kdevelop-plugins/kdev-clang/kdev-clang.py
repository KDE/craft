import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kdev-clang'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.shortDescription = "clang based c++ support for kdevelop"
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['extragear/kdevplatform'] = 'default'
        self.dependencies['testing/clang'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )

