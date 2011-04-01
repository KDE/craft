import info
import emergePlatform

class subinfo(info.infoclass):
    def setTargets( self ):
        #self.svnTargets['1.8.1'] = "http://mercurial.selenic.com/release/mercurial-1.8.1.tar.gz"
        #self.targetInstSrc['1.8.1'] = 'mercurial-1.8.1'
        self.targets['1.8.1'] = "http://mercurial.selenic.com/release/windows/Mercurial-1.8.1.exe"
        self.defaultTarget = '1.8.1'
        
from Package.SetupPackageBase import *

class Package(SetupPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        SetupPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
