import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "Runtime and library to organize the user work in separate activities"

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies['kde/kservice'] = 'default'
        self.dependencies['kde/kio'] = 'default'
        self.dependencies['win32libs/boost-headers'] = 'default'

        # those are only needed for building the activity manager daemon
#        self.dependencies['win32libs/boost-range'] = 'default'
#        self.dependencies['win32libs/boost-containers'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

