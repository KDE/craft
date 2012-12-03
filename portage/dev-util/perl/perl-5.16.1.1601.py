import info
import emergePlatform

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['5.8.8'] = "http://downloads.activestate.com/ActivePerl/Windows/5.8/ActivePerl-5.8.8.822-MSWin32-x86-280952.zip"
        self.targetMergeSourcePath['5.8.8'] = "ActivePerl-5.8.8.822-MSWin32-x86-280952\\perl"
        if emergePlatform.buildArchitecture() == 'x64':
           self.targets['5.10.1'] = "http://downloads.activestate.com/ActivePerl/releases/5.10.1.1007/ActivePerl-5.10.1.1007-MSWin32-x64-291969.zip"
           self.targetDigests['5.10.1'] = 'b5e9ab83d14e1c3311e280a96d355d491d4d55f5'
           self.targetMergeSourcePath['5.10.1'] = "ActivePerl-5.10.1.1007-MSWin32-x64-291969\\perl"
           self.targets['5.12.2'] = "http://downloads.activestate.com/ActivePerl/releases/5.12.2.1203/ActivePerl-5.12.2.1203-MSWin32-x64-294165.zip"
           #self.targetDigests['5.12.2'] = 'b5e9ab83d14e1c3311e280a96d355d491d4d55f5'
           self.targetMergeSourcePath['5.12.2'] = "ActivePerl-5.12.2.1203-MSWin32-x64-294165\\perl"
           self.targets['5.12.4'] = "http://downloads.activestate.com/ActivePerl/releases/5.12.4.1205/ActivePerl-5.12.4.1205-MSWin32-x64-294981.zip"
           self.targetDigests['5.12.4'] = 'f49d3681908978e1093f270cce0bf02d0a92334e'
           self.targetMergeSourcePath['5.12.4'] = "ActivePerl-5.12.4.1205-MSWin32-x64-294981\\perl"
           self.targets['5.16.1'] = "http://downloads.activestate.com/ActivePerl/releases/5.16.1.1601/ActivePerl-5.16.1.1601-MSWin32-x64-296175.zip"
           self.targetDigests['5.16.1'] = '2993227966574afb227640dcd139b088fee43879'
           self.targetMergeSourcePath['5.16.1'] = "ActivePerl-5.16.1.1601-MSWin32-x64-296175\\perl"
        else:
           self.targets['5.10.1'] = "http://downloads.activestate.com/ActivePerl/releases/5.10.1.1007/ActivePerl-5.10.1.1007-MSWin32-x86-291969.zip"
           self.targetDigests['5.10.1'] = '9122a828b32d8b8499c73b61972eaec303698961'
           self.targetMergeSourcePath['5.10.1'] = "ActivePerl-5.10.1.1007-MSWin32-x86-291969\\perl"
           self.targets['5.12.2'] = "http://downloads.activestate.com/ActivePerl/releases/5.12.2.1203/ActivePerl-5.12.2.1203-MSWin32-x86-294165.zip"
           self.targetDigests['5.12.2'] = 'f87d1ab5867a38a46a68f82f5a35d2d2526c1420'
           self.targetMergeSourcePath['5.12.2'] = "ActivePerl-5.12.2.1203-MSWin32-x86-294165\\perl"
           self.targets['5.12.4'] = "http://downloads.activestate.com/ActivePerl/releases/5.12.4.1205/ActivePerl-5.12.4.1205-MSWin32-x86-294981.zip"
           self.targetDigests['5.12.4'] = '14dc84b576a1004d8c71ca3309534c7952215182'
           self.targetMergeSourcePath['5.12.4'] = "ActivePerl-5.12.4.1205-MSWin32-x86-294981\\perl"
           self.targets['5.16.1'] = "http://downloads.activestate.com/ActivePerl/releases/5.16.1.1601/ActivePerl-5.16.1.1601-MSWin32-x86-296175.zip"
           self.targetDigests['5.16.1'] = 'e638f101c46ca8f0ecbfd7a07772d434d7c22c56'
           self.targetMergeSourcePath['5.16.1'] = "ActivePerl-5.16.1.1601-MSWin32-x86-296175\\perl"
        self.defaultTarget = '5.16.1'
    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'

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
