import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets["gitHEAD"] = 'https://github.com/zaphoyd/websocketpp.git'


        self.shortDescription = 'WebSocket++ is a header only C++ library that implements RFC6455 The WebSocket Protocol'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

