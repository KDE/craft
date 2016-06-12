import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )
        self.shortDescription = "KolourPaint is an easy-to-use paint program"
        self.svnTargets['master'] = "[git]kde:okular|frameworks"

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.dependencies['kdesupport/qimageblitz'] = 'default'
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.buildDependencies["libs/qtbase"] = "default"
        self.dependencies["frameworks/kconfig"] = "default"
        self.dependencies["frameworks/kdoctools"] = "default"
        self.dependencies["frameworks/kguiaddons"] = "default"
        self.dependencies["frameworks/kdelibs4support"] = "default"
        self.dependencies["frameworks/ki18n"] = "default"
        self.dependencies["frameworks/kinit"] = "default"
        self.dependencies["frameworks/kjobwidgets"] = "default"
        self.dependencies["frameworks/kio"] = "default"
        self.dependencies["frameworks/kparts"] = "default"
        self.dependencies["frameworks/ktexteditor"] = "default"
        self.dependencies["frameworks/kwindowsystem"] = "default"
        self.dependencies["frameworks/kxmlgui"] = "default"
        self.dependencies["frameworks/kdbusaddons"] = "default"
        self.dependencies["frameworks/threadweaver"] = "default"

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
