import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['5.8.8'] = "http://downloads.activestate.com/ActivePerl/Windows/5.8/ActivePerl-5.8.8.822-MSWin32-x86-280952.zip"
        self.targetMergeSourcePath['5.8.8'] = "ActivePerl-5.8.8.822-MSWin32-x86-280952\\perl"
        self.targets['5.10.0'] = "http://downloads.activestate.com/ActivePerl/Windows/5.10/ActivePerl-5.10.0.1004-MSWin32-x86-287188.zip"
        self.targetMergeSourcePath['5.10.0'] = "ActivePerl-5.10.0.1004-MSWin32-x86-287188\\perl"
        self.defaultTarget = '5.10.0'
        
from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
