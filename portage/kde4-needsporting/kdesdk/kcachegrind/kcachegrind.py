import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )
        self.shortDescription = "GUI to profilers such as Valgrind"
        self.defaultTarget = 'master'

    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['frameworks/karchive'] = 'default'
        self.dependencies['frameworks/kcoreaddons'] = 'default'
        self.dependencies['frameworks/kdoctools'] = 'default'
        self.dependencies['frameworks/kwidgetsaddons'] = 'default'
        self.dependencies['frameworks/kxmlgui'] = 'default'
        self.dependencies['frameworks/kdelibs4support'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__(self)

