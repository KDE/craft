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
        self.dependencies["libs/qttools"] = "default" # for Qt5Designer
        self.dependencies["frameworks/kitemviews"] = "default"
        self.dependencies["frameworks/kdelibs4support"] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__(self)

