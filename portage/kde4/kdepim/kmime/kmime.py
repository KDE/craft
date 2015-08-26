import info
import kdedefaults as kd
from EmergeConfig import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues()

        self.shortDescription = ""
        self.defaultTarget = 'master'

    def setDependencies( self ):
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies["libs/qtbase"] = "default"
        self.dependencies["win32libs/boost-headers"] = "default" # not searched by cmake
        self.dependencies["frameworks/ki18n"] = "default"
        self.dependencies["frameworks/kcodecs"] = "default"
        self.dependencies["frameworks/kdelibs4support"] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__(self)

