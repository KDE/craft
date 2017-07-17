import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['5.0'] = '[git]kde:kdev-python|5.0|'
        self.svnTargets['5.1'] = '[git]kde:kdev-python|5.1|'
        self.defaultTarget = 'master'

    def setDependencies( self ):
        self.shortDescription = "python support for kdevelop"
        self.runtimeDependencies['virtual/base'] = 'default'
        self.runtimeDependencies['extragear/kdevplatform'] = 'default'
        self.runtimeDependencies['extragear/kdevelop'] = 'default'
        self.runtimeDependencies['binary/python-libs'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )

