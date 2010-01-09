import info

class subinfo (info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        self.targets['0.9.21b'] = "http://downloads.sourceforge.net/sourceforge/clucene/clucene-core-0.9.21b.tar.bz2"
        self.patchToApply['0.9.21b'] = ('clucene-core-0.9.21-2.diff', 0)
        self.targetInstSrc['0.9.21b'] = "clucene-core-0.9.21b"
        self.defaultTarget = '0.9.21b'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
    
if __name__ == '__main__':
    Package().execute()
