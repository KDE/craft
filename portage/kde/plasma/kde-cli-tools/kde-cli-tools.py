import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )
        
    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['frameworks/kconfig'] = 'default'
        self.dependencies['frameworks/kinit'] = 'default'
        self.dependencies['frameworks/ki18n'] = 'default'
        self.dependencies["frameworks/kcmutils"] = 'default'
        self.dependencies['frameworks/kio'] = 'default'
        self.dependencies['frameworks/kwindowsystem'] = 'default'


from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )

