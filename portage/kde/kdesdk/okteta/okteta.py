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
        self.dependencies["frameworks/kbookmarks"] = "default"
        self.dependencies["frameworks/kcodecs"] = "default"
        self.dependencies["frameworks/kcompletion"] = "default"
        self.dependencies["frameworks/kconfigwidgets"] = "default"
        self.dependencies["frameworks/kdbusaddons"] = "default"
        self.dependencies["frameworks/kdoctools"] = "default"
        self.dependencies["frameworks/ki18n"] = "default"
        self.dependencies["frameworks/kcmutils"] = "default"
        self.dependencies["frameworks/kio"] = "default"
        self.dependencies["frameworks/knewstuff"] = "default"
        self.dependencies["frameworks/kparts"] = "default"
        self.dependencies["frameworks/kservice"] = "default"
        self.dependencies["frameworks/kwidgetsaddons"] = "default"
        self.dependencies["frameworks/kxmlgui"] = "default"
        #self.dependencies["kdesupport/qca"] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__(self)

