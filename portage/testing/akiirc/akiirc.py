from info import infoclass
from Package.CMakePackageBase import CMakePackageBase

class subinfo(infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:aki'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kdelibs'] = 'default'
        self.dependencies['win32libs/openssl'] = 'default'
        self.dependencies['win32libs/boost'] = 'default'
        # also needs icu from http://site.icu-project.org

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)

