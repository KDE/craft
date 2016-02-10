import info
import kdedefaults as kd
from EmergeConfig import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues()

        self.shortDescription = ""
        self.defaultTarget = 'master'

    def setDependencies( self ):
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.dependencies["libs/qtbase"] = "default"
        self.dependencies["frameworks/kcmutils"] = "default"
        self.dependencies["frameworks/kdelibs4support"] = "default"
        self.dependencies["kde/kcontacts"] = "default"
        self.dependencies["win32libs/openldap"] = "default"
        self.dependencies["win32libs/cyrus-sasl"] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__(self)

