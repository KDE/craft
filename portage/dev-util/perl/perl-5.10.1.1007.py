import info
import platform

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['5.8.8'] = "http://downloads.activestate.com/ActivePerl/Windows/5.8/ActivePerl-5.8.8.822-MSWin32-x86-280952.zip"
        self.targetMergeSourcePath['5.8.8'] = "ActivePerl-5.8.8.822-MSWin32-x86-280952\\perl"
        if platform.buildArchitecture() == 'x64':
           self.targets['5.10.1'] = "http://downloads.activestate.com/ActivePerl/releases/5.10.1.1007/ActivePerl-5.10.1.1007-MSWin32-x64-291969.zip"
           self.targetDigests['5.10.1'] = 'b5e9ab83d14e1c3311e280a96d355d491d4d55f5'
           self.targetMergeSourcePath['5.10.1'] = "ActivePerl-5.10.1.1007-MSWin32-x64-291969\\perl"   
        else:
           self.targets['5.10.1'] = "http://downloads.activestate.com/ActivePerl/releases/5.10.1.1007/ActivePerl-5.10.1.1007-MSWin32-x86-291969.zip"
           self.targetDigests['5.10.1'] = '9122a828b32d8b8499c73b61972eaec303698961'
           self.targetMergeSourcePath['5.10.1'] = "ActivePerl-5.10.1.1007-MSWin32-x86-291969\\perl"       
        self.defaultTarget = '5.10.1'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
