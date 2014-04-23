import info


class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['2.4.8'] = 'http://www.cmake.org/files/v2.4/cmake-2.4.8-win32-x86.zip'
        self.targets['2.6.4'] = 'http://www.cmake.org/files/v2.6/cmake-2.6.4-win32-x86.zip'
        self.targets['2.8.4'] = 'http://www.cmake.org/files/v2.8/cmake-2.8.4-win32-x86.zip'
        self.targets['2.8.5'] = 'http://www.cmake.org/files/v2.8/cmake-2.8.5-win32-x86.zip'
        self.targets['2.8.8'] = 'http://www.cmake.org/files/v2.8/cmake-2.8.8-win32-x86.zip'
        self.targets['2.8.12.1'] = 'http://www.cmake.org/files/v2.8/cmake-2.8.12.1-win32-x86.zip'
        self.targets['2.8.12.2'] = 'http://www.cmake.org/files/v2.8/cmake-2.8.12.2-win32-x86.zip'
        self.targets['v2.8.2'] = 'http://downloads.sourceforge.net/kde-windows/cmake-vc90-v2.8.2-bin.tar.bz2'
        self.targets['2.8.0-ce'] = 'http://downloads.sourceforge.net/kde-windows/cmake-vc90-2.8.0-6-bin.tar.bz2'
        self.targets['2.8.1-ce'] = 'http://downloads.sourceforge.net/kde-windows/cmake-vc90-2.8.1-bin.tar.bz2'
        self.targets['2.8.3-1'] = 'http://downloads.sourceforge.net/kde-windows/cmake-vc90-2.8.3-1-bin.tar.bz2'
        self.targets['2.8.3-2'] = 'http://downloads.sourceforge.net/kde-windows/cmake-vc90-2.8.3-2-bin.tar.bz2'
        self.targets['v2.8.8'] = 'http://downloads.sourceforge.net/kde-windows/cmake-vc100-2.8.8-bin.tar.bz2'
        self.targets['v2.8.10.2'] = 'http://downloads.sourceforge.net/kde-windows/cmake-x86-mingw4-2.8.10.2.7z'
        self.targetMergeSourcePath['2.4.8'] = 'cmake-2.4.8-win32-x86'
        self.targetMergeSourcePath['2.6.4'] = 'cmake-2.6.4-win32-x86'
        self.targetMergeSourcePath['2.8.4'] = 'cmake-2.8.4-win32-x86'
        self.targetMergeSourcePath['2.8.5'] = 'cmake-2.8.5-win32-x86'
        self.targetMergeSourcePath['2.8.8'] = 'cmake-2.8.8-win32-x86'
        self.targetMergeSourcePath['2.8.12.1'] = 'cmake-2.8.12.1-win32-x86'
        self.targetMergeSourcePath['2.8.12.2'] = 'cmake-2.8.12.2-win32-x86'
        self.targetDigests['v2.8.2'] = 'de516a570808c7a022139b55e758d5f7b378ec7d'
        self.targetDigests['2.8.3-2'] = 'cba746303abb825c8549e6621da35757c039fa9e'
        self.targetDigests['2.8.4'] = '539ce250521d964a8770e0a7362db196dbc97fbc'
        self.targetDigests['2.8.5'] = 'ffdcd882600fba4dee1c225d89831f2f889c8276'
        self.targetDigests['2.8.8'] = '3e93868b4be00e4cee1787c8d0479b2bf3807602'
        self.targetDigests['v2.8.8'] = 'd63da3b1790b64729e357c157ad9103e1bcfa267'
        self.targetDigests['v2.8.10.2'] = '56a5d0820e92c01c39ae2d9be38d3dfe459d4281'
        self.targetDigests['2.8.12.1'] = '6a27d8fcf887774e56fa165eddd5242e1c350464'
        self.targetDigests['2.8.12.2'] = '0d778fe630e623c881c14e1fef7b6ad40f68055c'
        self.patchToApply['v2.8.2'] = ( 'findtiff.diff', 0 )
        self.patchToApply['v2.8.10.2'] = ( 'findpng16.diff', 0 )

        self.defaultTarget = '2.8.12.2'


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
