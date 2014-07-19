import info
from EmergeConfig import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "the KDE text editor"
        self.defaultTarget = 'frameworks'

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.buildDependencies["libs/qtbase"] = "default"
        self.dependencies["kde/kconfig"] = "default"
        self.dependencies["kde/kdoctools"] = "default"
        self.dependencies["kde/kguiaddons"] = "default"
        self.dependencies["kde/ki18n"] = "default"
        self.dependencies["kde/kinit"] = "default"
        self.dependencies["kde/kjobwidgets"] = "default"
        self.dependencies["kde/kio"] = "default"
        self.dependencies["kde/kparts"] = "default"
        self.dependencies["kde/ktexteditor"] = "default"
        self.dependencies["kde/kwindowsystem"] = "default"
        self.dependencies["kde/kxmlgui"] = "default"
        self.dependencies["kde/kdbusaddons"] = "default"
        self.dependencies["kde/kitemmodels"] = "default"

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DBUILD_doc=OFF "
