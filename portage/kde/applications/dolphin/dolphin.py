import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )


    def setDependencies( self ):
        self.runtimeDependencies['libs/qtbase'] = 'default'
        self.runtimeDependencies['frameworks/kdoctools'] = 'default'
        self.runtimeDependencies['frameworks/kinit'] = 'default'
        self.runtimeDependencies['frameworks/kcmutils'] = 'default'
        self.runtimeDependencies['frameworks/knewstuff'] = 'default'
        self.runtimeDependencies['frameworks/kcoreaddons' ] = 'default'
        self.runtimeDependencies['frameworks/ki18n'] = 'default'
        self.runtimeDependencies['frameworks/kdbusaddons'] = 'default'
        self.runtimeDependencies['frameworks/kbookmarks'] = 'default'
        self.runtimeDependencies['frameworks/kconfig'] = 'default'
        self.runtimeDependencies['frameworks/kio'] = 'default'
        self.runtimeDependencies['frameworks/kparts'] = 'default'
        self.runtimeDependencies['frameworks/solid'] = 'default'
        self.runtimeDependencies['frameworks/kiconthemes'] = 'default'
        self.runtimeDependencies['frameworks/kcompletion'] = 'default'
        self.runtimeDependencies['frameworks/ktexteditor'] = 'default'
        self.runtimeDependencies['frameworks/kwindowsystem'] = 'default'
        self.runtimeDependencies['frameworks/knotifications'] = 'default'
        self.runtimeDependencies['frameworks/kdelibs4support'] = 'default'

        

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

