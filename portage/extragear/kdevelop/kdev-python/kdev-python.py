import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

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
