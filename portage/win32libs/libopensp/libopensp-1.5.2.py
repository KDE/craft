import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['1.5.2'] = "http://downloads.sourceforge.net/project/openjade/opensp/1.5.2/OpenSP-1.5.2.tar.gz"
        self.targetInstSrc['1.5.2'] = "OpenSP-1.5.2"
        self.patchToApply['1.5.2'] = ( "OpenSP-1.5.2-20110111.diff", 1)
        self.targetDigests['1.5.2'] = 'b4e903e980f8a8b3887396a24e067bef126e97d5'
        self.shortDescription = "a library for a SGML parser algorithm"
        self.defaultTarget = '1.5.2'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

