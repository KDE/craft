import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )


    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['frameworks/kdoctools'] = 'default'
        self.dependencies['frameworks/kinit'] = 'default'
        self.dependencies['frameworks/kcmutils'] = 'default'
        self.dependencies['frameworks/knewstuff'] = 'default'
        self.dependencies['frameworks/kcoreaddons' ] = 'default'
        self.dependencies['frameworks/ki18n'] = 'default'
        self.dependencies['frameworks/kdbusaddons'] = 'default'
        self.dependencies['frameworks/kbookmarks'] = 'default'
        self.dependencies['frameworks/kconfig'] = 'default'
        self.dependencies['frameworks/kio'] = 'default'
        self.dependencies['frameworks/kparts'] = 'default'
        self.dependencies['frameworks/solid'] = 'default'
        self.dependencies['frameworks/kiconthemes'] = 'default'
        self.dependencies['frameworks/kcompletion'] = 'default'
        self.dependencies['frameworks/ktexteditor'] = 'default'
        self.dependencies['frameworks/kwindowsystem'] = 'default'
        self.dependencies['frameworks/knotifications'] = 'default'
        
        self.dependencies['kde/baloo'] = 'default'
        
        

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

