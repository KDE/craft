import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['5.0'] = '[git]kde:kdevplatform|5.0'
        self.svnTargets['5.1'] = '[git]kde:kdevplatform|5.1'
        self.svnTargets['master'] = '[git]kde:kdevplatform|master'
        self.shortDescription = 'Framework to build IDE-like applications'
        self.defaultTarget = 'master'

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.buildDependencies["dev-util/zip"] = "default"
        self.buildDependencies["win32libs/boost-headers"] = "default"
        self.runtimeDependencies["libs/qtscript"] = "default"
        self.runtimeDependencies["libs/qtquickcontrols"] = "default"
        self.runtimeDependencies["libs/qtwebengine"] = "default"
        self.runtimeDependencies["libs/qtbase"] = "default"
        self.runtimeDependencies[ 'frameworks/karchive' ] = 'default'
        self.runtimeDependencies[ 'frameworks/kconfig' ] = 'default'
        self.runtimeDependencies[ 'frameworks/kguiaddons' ] = 'default'
        self.runtimeDependencies[ 'frameworks/ki18n' ] = 'default'
        self.runtimeDependencies[ 'frameworks/kitemmodels' ] = 'default'
        self.runtimeDependencies[ 'frameworks/kitemviews' ] = 'default'
        self.runtimeDependencies[ 'frameworks/kjobwidgets' ] = 'default'
        self.runtimeDependencies[ 'frameworks/kcmutils' ] = 'default'
        self.runtimeDependencies[ 'frameworks/knewstuff' ] = 'default'
        self.runtimeDependencies[ 'frameworks/knotifyconfig' ] = 'default'
        self.runtimeDependencies[ 'frameworks/kparts' ] = 'default'
        self.runtimeDependencies[ 'frameworks/kservice' ] = 'default'
        self.runtimeDependencies[ 'frameworks/sonnet' ] = 'default'
        self.runtimeDependencies[ 'frameworks/ktexteditor' ] = 'default'
        self.runtimeDependencies[ 'frameworks/threadweaver' ] = 'default'
        self.runtimeDependencies[ 'frameworks/kwindowsystem' ] = 'default'
        self.runtimeDependencies[ 'frameworks/kxmlgui' ] = 'default'
        self.runtimeDependencies[ 'frameworks/kdeclarative' ] = 'default'
        self.runtimeDependencies[ 'kde/libkomparediff2' ] = 'default'
        self.runtimeDependencies[ 'kdesupport/grantlee' ] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self):
        CMakePackageBase.__init__( self )

