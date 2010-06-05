import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['4.0-beta1'] = 'http://downloads.sourceforge.net/libmsn/libmsn-4.0-beta1.tar.bz2'
        self.targets['4.0-beta2'] = 'http://downloads.sourceforge.net/libmsn/libmsn-4.0-beta2.tar.bz2'
        self.targets['4.0-beta4'] = 'http://downloads.sourceforge.net/libmsn/libmsn-4.0-beta4.tar.bz2'
        self.targets['4.0-beta7'] = 'http://downloads.sourceforge.net/libmsn/libmsn-4.0-beta7.tar.bz2'
        self.targets['4.0-beta8'] = 'http://downloads.sourceforge.net/libmsn/libmsn-4.0-beta8.tar.bz2'
        self.targets['4.0'] = 'http://downloads.sourceforge.net/libmsn/libmsn-4.0.tar.bz2'
        self.targetInstSrc['4.0-beta1'] = 'libmsn-4.0-beta1'
        self.targetInstSrc['4.0-beta2'] = 'libmsn-4.0-beta2'
        self.targetInstSrc['4.0-beta4'] = 'libmsn-4.0-beta4'
        self.targetInstSrc['4.0-beta7'] = 'libmsn-4.0-beta7'
        self.targetInstSrc['4.0-beta8'] = 'libmsn-4.0-beta8'
        self.targetInstSrc['4.0'] = 'libmsn-4.0'
        self.patchToApply['4.0-beta1'] = ('libmsn.diff', 0)
        self.patchToApply['4.0-beta2'] = ('libmsn_b2.diff', 0)
        self.patchToApply['4.0-beta4'] = ('libmsn_b4.diff', 0)
        self.defaultTarget = '4.0'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['win32libs-bin/openssl'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()