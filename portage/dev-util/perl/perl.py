import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['5.8.8'] = "http://downloads.activestate.com/ActivePerl/Windows/5.8/ActivePerl-5.8.8.822-MSWin32-x86-280952.zip"
        self.targetMergeSourcePath['5.8.8'] = "ActivePerl-5.8.8.822-MSWin32-x86-280952\\perl"
        if compiler.isX64():
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
           self.targets['5.16.3'] = "http://downloads.activestate.com/ActivePerl/releases/5.16.3.1603/ActivePerl-5.16.3.1603-MSWin32-x64-296746.zip"
           self.targetDigests['5.16.3'] = '9cae0a0e24a86a26814206ff1bf02a7e7cfea4ba'
           self.targetMergeSourcePath['5.16.3'] = "ActivePerl-5.16.3.1603-MSWin32-x64-296746\\perl"
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
           self.targets['5.16.3'] = "http://downloads.activestate.com/ActivePerl/releases/5.16.3.1603/ActivePerl-5.16.3.1603-MSWin32-x86-296746.zip"
           self.targetDigests['5.16.3'] = 'c85063396993a6bf4989970585b0d3a21c7a2a8c'
           self.targetMergeSourcePath['5.16.3'] = "ActivePerl-5.16.3.1603-MSWin32-x86-296746\\perl"
        self.defaultTarget = '5.16.3'

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'


from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.merge.destinationPath = "dev-utils"
        self.subinfo.options.merge.ignoreBuildType = True

if __name__ == '__main__':
    Package().execute()
