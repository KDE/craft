import info
import kdedefaults as kd
from EmergeConfig import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues()
        self.defaultTarget = "frameworks"

    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'
        self.shortDescription = "KDE base applications (Konqueror, Dolphin)"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )

