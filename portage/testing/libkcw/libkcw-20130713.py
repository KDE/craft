import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:libkcw'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.shortDescription = "a support toolkit to minimally wrap Windows API"
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
