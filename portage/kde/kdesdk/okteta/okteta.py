import info
import kdedefaults as kd
from EmergeConfig import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues()

        self.shortDescription = "KDE hex editor for viewing and editing the raw data of files."
        self.defaultTarget = 'frameworks'

    def setDependencies( self ):
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies["libs/qtbase"] = "default"
        self.dependencies["kde/kbookmarks"] = "default"
        self.dependencies["kde/kcodecs"] = "default"
        self.dependencies["kde/kcompletion"] = "default"
        self.dependencies["kde/kconfigwidgets"] = "default"
        self.dependencies["kde/kdbusaddons"] = "default"
        self.dependencies["kde/kdoctools"] = "default"
        self.dependencies["kde/ki18n"] = "default"
        self.dependencies["kde/kcmutils"] = "default"
        self.dependencies["kde/kio"] = "default"
        self.dependencies["kde/knewstuff"] = "default"
        self.dependencies["kde/kparts"] = "default"
        self.dependencies["kde/kservice"] = "default"
        self.dependencies["frameworks/kwidgetsaddons"] = "default"
        self.dependencies["kde/kxmlgui"] = "default"
        #self.dependencies["kdesupport/qca"] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__(self)

