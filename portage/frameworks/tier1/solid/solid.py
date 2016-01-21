import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "Solid"
        

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies["libs/qtbase"] = "default"
        self.dependencies["libs/qttools"] = "default"
        self.dependencies["libs/qtdeclarative"] = "default"
from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )

        # Disable multi job build for now
        # CMake / Solid CMake code bug, we don't know
        #
        # moc: Cannot create R:/build/frameworks/solid/work/msvc2015-RelWithDebInfo-master/src/solid/moc_devicemanager.cpp
        # AUTOGEN: error: process for R:/build/frameworks/solid/work/msvc2015-RelWithDebInfo-master/src/solid/moc_devicemanager.cpp failed:
        #     moc: Cannot create R:/build/frameworks/solid/work/msvc2015-RelWithDebInfo-master/src/solid/moc_devicemanager.cpp
        #     moc failed...
        self.subinfo.options.make.supportsMultijob = False
