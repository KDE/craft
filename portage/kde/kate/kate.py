import info
from EmergeConfig import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "the KDE text editor"
        self.defaultTarget = 'master'

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.buildDependencies["libs/qtbase"] = "default"
        self.dependencies["frameworks/kconfig"] = "default"
        self.dependencies["frameworks/kdoctools"] = "default"
        self.dependencies["frameworks/kguiaddons"] = "default"
        self.dependencies["frameworks/ki18n"] = "default"
        self.dependencies["frameworks/kinit"] = "default"
        self.dependencies["frameworks/kjobwidgets"] = "default"
        self.dependencies["frameworks/kio"] = "default"
        self.dependencies["frameworks/kparts"] = "default"
        self.dependencies["frameworks/ktexteditor"] = "default"
        self.dependencies["frameworks/kwindowsystem"] = "default"
        self.dependencies["frameworks/kxmlgui"] = "default"
        self.dependencies["frameworks/kdbusaddons"] = "default"
        self.dependencies["frameworks/kitemmodels"] = "default"

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DBUILD_doc=OFF -DBUILD_addons=OFF"
