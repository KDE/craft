import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kinfocenter'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['frameworks/ki18n'] = 'default'
        self.dependencies['frameworks/kiconthemes'] = 'default'
        self.dependencies['frameworks/kcmutils'] = 'default'
        self.dependencies['frameworks/solid'] = 'default'
        self.dependencies['frameworks/plasma'] = 'default'
        self.dependencies['frameworks/solid'] = 'default'
        self.dependencies['frameworks/kwindowsystem'] = 'default'
        self.dependencies['frameworks/kdelibs4support'] = 'default'



from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )

