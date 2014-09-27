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
        self.dependencies[ 'kde/kjobwidgets' ] = 'default'
        self.dependencies[ 'kde/kcmutils' ] = 'default'
        self.dependencies[ 'kde/knewstuff' ] = 'default'
        self.dependencies[ 'kde/knotifyconfig' ] = 'default'
        self.dependencies[ 'kde/kparts' ] = 'default'
        self.dependencies[ 'kde/kservice' ] = 'default'
        self.dependencies[ 'frameworks/sonnet' ] = 'default'
        self.dependencies[ 'kde/ktexteditor' ] = 'default'
        self.dependencies[ 'frameworks/threadweaver' ] = 'default'
        self.dependencies[ 'frameworks/kwindowsystem' ] = 'default'
        self.dependencies[ 'kde/kxmlgui' ] = 'default'
        self.dependencies[ 'kde/kdelibs4support' ] = 'default'
        self.dependencies[ 'kde/libkomparediff2' ] = 'default'
	# krunner is an optional dependency now
        #self.dependencies[ 'kde/krunner' ] = 'default'
        self.dependencies[ 'extragear/kdevplatform' ] = 'default'


from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self):
        CMakePackageBase.__init__( self )

