import info
from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:libkface'
        self.defaultTarget = 'gitHEAD'
        self.shortDescription = "a Qt/C++ wrapper around LibFace library to perform face recognition and detection over pictures"

    def setDependencies( self ):
        self.dependencies['virtual/kde-runtime'] = 'default'
        self.dependencies['win32libs-bin/opencv'] = 'default'

class Package( CMakePackageBase ):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
