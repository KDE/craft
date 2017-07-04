import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )
        self.shortDescription = "GUI to profilers such as Valgrind"
        self.defaultTarget = 'master'

    def setDependencies( self ):
        self.runtimeDependencies['libs/qtbase'] = 'default'
        self.runtimeDependencies['frameworks/karchive'] = 'default'
        self.runtimeDependencies['frameworks/kcoreaddons'] = 'default'
        self.runtimeDependencies['frameworks/kdoctools'] = 'default'
        self.runtimeDependencies['frameworks/kwidgetsaddons'] = 'default'
        self.runtimeDependencies['frameworks/kxmlgui'] = 'default'
        self.runtimeDependencies['frameworks/kdelibs4support'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__(self)

