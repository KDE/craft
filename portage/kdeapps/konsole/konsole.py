import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:konsole'
        self.svnTargets['winport'] = '[git]kde:konsole|winport-frameworks|'
        self.defaultTarget = 'winport'

    def setDependencies( self ):
        self.dependencies['testing/kcwsh'] = 'default'
        self.dependencies['kde/kbookmarks'] = 'default'
        self.dependencies['kde/kinit'] = 'default'
        self.dependencies['kde/kdelibs4support'] = 'default'
        self.dependencies['kde/knotifyconfig'] = 'default'


from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DBUILD_doc=OFF "

