import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )
        
    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['frameworks/ki18n'] = 'default'
        self.dependencies['frameworks/kconfig'] = 'default'
        self.dependencies['frameworks/kconfigwidgets'] = 'default'
        self.dependencies['frameworks/kdbusaddons'] = 'default'
        self.dependencies['frameworks/kcoreaddons'] = 'default'
        self.dependencies['frameworks/kcmutils'] = 'default'
        self.dependencies['frameworks/kio'] = 'default'
        self.dependencies['frameworks/kdelibs4support'] = 'default'
        self.dependencies['frameworks/kxmlgui'] = 'default'
        self.dependencies['frameworks/kiconthemes'] = 'default'
        self.dependencies['frameworks/kservice'] = 'default'
        self.dependencies['frameworks/kcompletion'] = 'default'
        self.dependencies['frameworks/kdeclarative'] = 'default'
        self.dependencies['frameworks/kpackage'] = 'default'
        self.dependencies['frameworks/solid'] = 'default'



from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )

