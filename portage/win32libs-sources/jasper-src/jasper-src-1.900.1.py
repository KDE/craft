import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets[ '1.900.1-2' ] = 'http://www.ece.uvic.ca/~mdadams/jasper/software/jasper-1.900.1.zip'
        self.targetInstSrc[ '1.900.1-2' ] = os.path.join( 'jasper-1.900.1', 'src', 'libjasper' )
        self.patchToApply[ '1.900.1-2' ] = ( "jasper-1.900.1-20100430.diff", 3 )
        self.defaultTarget = '1.900.1-2'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs-bin/jpeg'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
