import info
import emergePlatform

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.5.0'] = "https://launchpad.net/bzr/2.5/2.5.0/+download/bzr-2.5.0-2-setup.exe"
        self.targetDigests['2.5.0'] = "2aacc8bb08747af824e1184496e440b5bf78f0d8"
        self.defaultTarget = '2.5.0'

from Package.SetupPackageBase import *

class Package(SetupPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        SetupPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
