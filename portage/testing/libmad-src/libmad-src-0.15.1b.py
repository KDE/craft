import os
import shutil
import utils
import info

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.15.1b'] = 'ftp://ftp.mars.org/pub/mpeg/libmad-0.15.1b.tar.gz'
        self.targetDigests['0.15.1b'] = 'cac19cd00e1a907f3150cc040ccc077783496d76'
        self.patchToApply['0.15.1b'] = ('libmad-src-0.15.1b-20101104.diff', 1)
        self.targetInstSrc['0.15.1b'] = 'libmad-0.15.1b'
        self.defaultTarget = '0.15.1b'       
                
class Package(CMakePackageBase):
    def __init__( self ):
        # we use subinfo for now too 
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )        

if __name__ == '__main__':
    Package().execute()

