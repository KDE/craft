import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['4.0'] = 'http://downloads.sourceforge.net/libmsn/libmsn-4.0.tar.bz2'
        self.targets['4.1'] = 'http://downloads.sourceforge.net/libmsn/libmsn-4.1.tar.bz2'
        self.targetInstSrc['4.0'] = 'libmsn-4.0'
        self.targetInstSrc['4.1'] = 'libmsn-4.1'
        self.patchToApply['4.0'] = ('libmsn-4.0-20101012.diff', 1)
        self.patchToApply['4.1'] = ('libmsn-4.1-20101012.diff', 1)
        self.defaultTarget = '4.1'

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