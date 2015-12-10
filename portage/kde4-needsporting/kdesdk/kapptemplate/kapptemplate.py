import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )
        self.shortDescription = "Factory for the easy creation of KDE/Qt components and programs"
        self.defaultTarget = 'master'

    def setDependencies( self ):
        self.dependencies['frameworks/kcoreaddons'] = 'default'
        self.dependencies['frameworks/kconfigwidgets'] = 'default'
        self.dependencies['frameworks/kcompletion'] = 'default'
        self.dependencies['frameworks/karchive'] = 'default'
        self.dependencies['frameworks/kio'] = 'default'
        self.dependencies['frameworks/ki18n'] = 'default'
        self.dependencies['frameworks/kdoctools'] = 'default'
        self.dependencies['dev-util/7zip'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__(self)

