import info
import os
from Package.CMakePackageBase import *
 
class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:qtopenal'
        self.defaultTarget = 'gitHEAD'
 
    def setDependencies( self ):
        self.dependencies['libs/qt'] = 'default'
        self.dependencies['testing/openal-soft-src'] = 'default'
        self.dependencies['win32libs/libsndfile'] = 'default'
 
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
 
if __name__ == '__main__':
    Package().execute()


