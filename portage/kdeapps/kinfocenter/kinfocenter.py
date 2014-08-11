import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kinfocenter'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['kde/ki18n'] = 'default'
        self.dependencies['kde/kiconthemes'] = 'default'
        self.dependencies['kde/kcmutils'] = 'default'
        self.dependencies['kde/solid'] = 'default'
        self.dependencies['kde/plasma'] = 'default'
        self.dependencies['kde/solid'] = 'default'
        self.dependencies['kde/kwindowsystem'] = 'default'
        self.dependencies['kde/kdelibs4support'] = 'default'



from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )

