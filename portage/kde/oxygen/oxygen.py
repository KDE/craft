import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:oxygen'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['kde/ki18n'] = 'default'
        self.dependencies['kde/kconfig'] = 'default'
        self.dependencies['frameworks/kguiaddons'] = 'default'
        self.dependencies["frameworks/kwidgetsaddons"] = 'default'
        self.dependencies['kde/kservice'] = 'default'
        self.dependencies['kde/kcompletion'] = 'default'
        self.dependencies['kde/frameworkintegration'] = 'default'
        self.dependencies['kde/kwindowsystem'] = 'default'



from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )

