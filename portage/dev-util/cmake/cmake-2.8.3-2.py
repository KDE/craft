import info
import emergePlatform

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['2.4.8'] = 'http://www.cmake.org/files/v2.4/cmake-2.4.8-win32-x86.zip'
        self.targets['2.6.4'] = 'http://www.cmake.org/files/v2.6/cmake-2.6.4-win32-x86.zip'
        self.targets['2.8.4'] = 'http://www.cmake.org/files/v2.8/cmake-2.8.4-win32-x86.zip'
        self.targets['v2.8.2'] = 'http://downloads.sourceforge.net/kde-windows/cmake-vc90-v2.8.2-bin.tar.bz2'
        self.targets['2.8.0-ce'] = 'http://downloads.sourceforge.net/kde-windows/cmake-vc90-2.8.0-6-bin.tar.bz2'
        self.targets['2.8.1-ce'] = 'http://downloads.sourceforge.net/kde-windows/cmake-vc90-2.8.1-bin.tar.bz2'
        self.targets['2.8.3-1'] = 'http://downloads.sourceforge.net/kde-windows/cmake-vc90-2.8.3-1-bin.tar.bz2'
        self.targets['2.8.3-2'] = 'http://downloads.sourceforge.net/kde-windows/cmake-vc90-2.8.3-2-bin.tar.bz2'
        self.targetMergeSourcePath['2.4.8'] = 'cmake-2.4.8-win32-x86'
        self.targetMergeSourcePath['2.6.4'] = 'cmake-2.6.4-win32-x86'
        self.targetMergeSourcePath['2.8.4'] = 'cmake-2.8.4-win32-x86'
        self.targetDigests['v2.8.2'] = 'de516a570808c7a022139b55e758d5f7b378ec7d'
        self.targetDigests['2.8.3-2'] = 'cba746303abb825c8549e6621da35757c039fa9e'
        self.targetDigests['2.8.4'] = '539ce250521d964a8770e0a7362db196dbc97fbc'
        self.patchToApply['v2.8.2'] = ( 'findtiff.diff', 0 )

        if emergePlatform.isCrossCompilingEnabled():
            self.defaultTarget = '2.8.0-ce'
        else:
            # 2.8.4 is broken when using short paths and
            # windres fails even in old projects like zlib
            self.defaultTarget = '2.8.3-2'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base']       = 'default'
        self.buildDependencies['gnuwin32/patch'] = 'default'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
