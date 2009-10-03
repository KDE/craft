import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['2.4.8'] = 'http://www.cmake.org/files/v2.4/cmake-2.4.8-win32-x86.zip'
        self.targets['2.6.4'] = 'http://www.cmake.org/files/v2.6/cmake-2.6.4-win32-x86.zip'
        self.targets['2.8.0-rc2'] = 'http://www.cmake.org/files/v2.8/cmake-2.8.0-rc2-win32-x86.zip'
        self.targetMergeSourcePath['2.4.8'] = 'cmake-2.4.8-win32-x86'
        self.targetMergeSourcePath['2.6.4'] = 'cmake-2.6.4-win32-x86'
        self.targetMergeSourcePath['2.8.0-rc2'] = 'cmake-2.8.0-rc2-win32-x86'
        self.defaultTarget = '2.6.4'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
