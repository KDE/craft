import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:systemsettings'
        self.defaultTarget = 'gitHEAD'

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



from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )

