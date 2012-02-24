import info
from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:libkgeomap'
        self.defaultTarget = 'gitHEAD'
        self.shortDescription = "a wrapper around different world-map components"

    def setDependencies( self ):
        self.dependencies['virtual/kde-runtime'] = 'default'
        self.dependencies['kde/marble'] = 'default'

class Package( CMakePackageBase ):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
