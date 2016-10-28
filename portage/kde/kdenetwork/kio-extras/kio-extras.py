import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )
        
        self.shortDescription = "Extra plugins for KIO (thumbnail generators, archives, remote filesystems and more)"
        
    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['frameworks/kactivities'] = 'default'
        self.dependencies['frameworks/karchive'] = 'default'
        self.dependencies['frameworks/kbookmarks'] = 'default'
        self.dependencies['frameworks/kconfig'] = 'default'
        self.dependencies['frameworks/kconfigwidgets'] = 'default'
        self.dependencies['frameworks/kcoreaddons'] = 'default'
        self.dependencies['frameworks/kdbusaddons'] = 'default'
        self.dependencies['frameworks/kdoctools'] = 'default'
        self.dependencies['frameworks/kdnssd'] = 'default'
        self.dependencies['frameworks/kguiaddons'] = 'default'
        self.dependencies['frameworks/kiconthemes'] = 'default'
        self.dependencies['frameworks/ki18n'] = 'default'
        self.dependencies['frameworks/kio'] = 'default'
        self.dependencies['frameworks/khtml'] = 'default'
        self.dependencies['frameworks/kdelibs4support'] = 'default'
        self.dependencies['frameworks/solid'] = 'default'
# Would be nice, but... yeah, pty on windows may happen, but not yet
#        self.dependencies['frameworks/kpty'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__(self)
