import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['master'] = '[git]kde:kdev-ruby'
        self.defaultTarget = 'master'

    def setDependencies( self ):
        self.shortDescription = "ruby support for kdevelop"
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['dev-util/winflexbison'] = 'default'
        self.dependencies['extragear/kdevplatform'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )

