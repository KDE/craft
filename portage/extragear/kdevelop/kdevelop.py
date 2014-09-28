import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ 'gitHEAD' ] = '[git]kde:kdevelop'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.buildDependencies["dev-util/zip"] = "default"
        self.dependencies["libs/qtbase"] = "default"
        self.dependencies["libs/qtdeclarative"] = "default"
        self.dependencies["libs/qtscript"] = "default"
        self.dependencies["libs/qtwebkit"] = "default"
        self.dependencies[ 'frameworks/karchive' ] = 'default'
        self.dependencies[ 'frameworks/kconfig' ] = 'default'
        self.dependencies[ 'frameworks/kguiaddons' ] = 'default'
        self.dependencies[ 'frameworks/ki18n' ] = 'default'
        self.dependencies[ 'frameworks/kitemmodels' ] = 'default'
        self.dependencies[ 'frameworks/kitemviews' ] = 'default'
        self.dependencies[ 'frameworks/kjobwidgets' ] = 'default'
        self.dependencies[ 'frameworks/kcmutils' ] = 'default'
        self.dependencies[ 'frameworks/knewstuff' ] = 'default'
        self.dependencies[ 'frameworks/knotifyconfig' ] = 'default'
        self.dependencies[ 'frameworks/kparts' ] = 'default'
        self.dependencies[ 'frameworks/kservice' ] = 'default'
        self.dependencies[ 'frameworks/sonnet' ] = 'default'
        self.dependencies[ 'frameworks/ktexteditor' ] = 'default'
        self.dependencies[ 'frameworks/threadweaver' ] = 'default'
        self.dependencies[ 'frameworks/kwindowsystem' ] = 'default'
        self.dependencies[ 'frameworks/kxmlgui' ] = 'default'
        self.dependencies[ 'frameworks/kdelibs4support' ] = 'default'
        self.dependencies[ 'kde/libkomparediff2' ] = 'default'
	# krunner is an optional dependency now
        #self.dependencies[ 'frameworks/krunner' ] = 'default'
        self.dependencies[ 'extragear/kdevplatform' ] = 'default'


from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self):
        CMakePackageBase.__init__( self )

