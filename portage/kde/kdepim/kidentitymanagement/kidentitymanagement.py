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
        self.dependencies["frameworks/kcoreaddons"] = "default"
        self.dependencies["frameworks/kcompletion"] = "default"
        self.dependencies["frameworks/ktextwidgets"] = "default"
        self.dependencies["frameworks/kxmlgui"] = "default"
        self.dependencies["frameworks/kio"] = "default"
        self.dependencies["frameworks/kconfig"] = "default"
        self.dependencies["frameworks/kemoticons"] = "default"
        self.dependencies["frameworks/kcodecs"] = "default"
        self.dependencies["frameworks/kdelibs4support"] = "default"
        self.dependencies["kde/kpimtextedit"] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__(self)

