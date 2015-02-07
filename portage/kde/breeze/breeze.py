import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )
        self.targets[ '5.2.0' ] = "ftp://ftp.kde.org/pub/kde/stable/plasma/5.2.0/breeze-5.2.0.tar.xz"
        self.targetInstSrc[ '5.2.0' ] = "breeze-5.2.0"
        self.defaultTarget = "5.2.0"


    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['frameworks/ki18n'] = 'default'
        self.dependencies['frameworks/kconfig'] = 'default'
        self.dependencies['frameworks/kguiaddons'] = 'default'
        self.dependencies["frameworks/kwidgetsaddons"] = 'default'
        self.dependencies['frameworks/kservice'] = 'default'
        self.dependencies['frameworks/kcompletion'] = 'default'
        self.dependencies['frameworks/frameworkintegration'] = 'default'
        self.dependencies['frameworks/kwindowsystem'] = 'default'
        self.dependencies['frameworks/kdecoration'] = 'default'


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

