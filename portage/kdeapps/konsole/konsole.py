import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:konsole'
        self.svnTargets['winport'] = '[git]kde:konsole|winport-frameworks|'
        self.defaultTarget = 'winport'

    def setDependencies( self ):
        # self.dependencies['kde/kdelibs'] = 'default'
        self.dependencies['testing/kcwsh'] = 'default'
        self.dependencies['kde/kbookmarks'] = 'default'
        # self.runtimeDependencies['kde/kde-runtime'] = 'default'


from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DBUILD_doc=OFF "

