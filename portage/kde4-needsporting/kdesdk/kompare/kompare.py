import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )
        self.shortDescription = "Graphical File Differences Tool"
        self.defaultTarget = 'master'

    def setDependencies( self ):
        self.dependencies['kde/libkomparediff2'] = 'default'
        self.dependencies['frameworks/kcoreaddons'] = 'default'
        self.dependencies['frameworks/kcodecs'] = 'default'
        self.dependencies['frameworks/kdoctools'] = 'default'
        self.dependencies['frameworks/kiconthemes'] = 'default'
        self.dependencies['frameworks/kjobwidgets'] = 'default'
        self.dependencies['frameworks/kconfig'] = 'default'
        self.dependencies['frameworks/kparts'] = 'default'
        self.dependencies['frameworks/ktexteditor'] = 'default'
        self.dependencies['frameworks/kwidgetsaddons'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__(self)

