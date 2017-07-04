import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )
        
        self.shortDescription = "Extra plugins for KIO (thumbnail generators, archives, remote filesystems and more)"
        
    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies['libs/qtbase'] = 'default'
        self.runtimeDependencies['frameworks/kactivities'] = 'default'
        self.runtimeDependencies['frameworks/karchive'] = 'default'
        self.runtimeDependencies['frameworks/kbookmarks'] = 'default'
        self.runtimeDependencies['frameworks/kconfig'] = 'default'
        self.runtimeDependencies['frameworks/kconfigwidgets'] = 'default'
        self.runtimeDependencies['frameworks/kcoreaddons'] = 'default'
        self.runtimeDependencies['frameworks/kdbusaddons'] = 'default'
        self.runtimeDependencies['frameworks/kdoctools'] = 'default'
        self.runtimeDependencies['frameworks/kdnssd'] = 'default'
        self.runtimeDependencies['frameworks/kguiaddons'] = 'default'
        self.runtimeDependencies['frameworks/kiconthemes'] = 'default'
        self.runtimeDependencies['frameworks/ki18n'] = 'default'
        self.runtimeDependencies['frameworks/kio'] = 'default'
        self.runtimeDependencies['frameworks/khtml'] = 'default'
        self.runtimeDependencies['frameworks/solid'] = 'default'
# Would be nice, but... yeah, pty on windows may happen, but not yet
#        self.runtimeDependencies['frameworks/kpty'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__(self)
