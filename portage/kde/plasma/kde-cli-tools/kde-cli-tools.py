import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )
        
    def setDependencies( self ):
        self.runtimeDependencies['libs/qtbase'] = 'default'
        self.runtimeDependencies['frameworks/kconfig'] = 'default'
        self.runtimeDependencies['frameworks/kinit'] = 'default'
        self.runtimeDependencies['frameworks/ki18n'] = 'default'
        self.runtimeDependencies["frameworks/kcmutils"] = 'default'
        self.runtimeDependencies['frameworks/kio'] = 'default'
        self.runtimeDependencies['frameworks/kwindowsystem'] = 'default'


from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )

