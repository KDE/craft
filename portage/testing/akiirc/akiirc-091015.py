from info import infoclass
from Package.CMakePackageBase import CMakePackageBase

class subinfo(infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:aki'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.hardDependencies['kde/kdelibs'] = 'default'
        self.hardDependencies['win32libs/openssl'] = 'default'
        self.hardDependencies['win32libs/boost'] = 'default'
        # also needs icu from http://site.icu-project.org

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
