import os
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        for ver in ['2.0.1', '2.1.0-beta3', '2.1.0']:
            self.targets[ ver ] = 'http://downloads.sourceforge.net/sourceforge/expat/expat-' + ver + '.tar.gz'
            self.targetInstSrc[ ver ] = 'expat-' + ver
        self.targetInstSrc[ '2.1.0-beta3' ] = 'expat-2012-03-11'
        self.patchToApply['2.0.1'] = ('expat-2.0.1-20100329.diff', 1)
        self.patchToApply['2.1.0'] = ('expat-2.1.0-20130311.diff', 1)
        self.targetDigests['2.0.1'] = '663548c37b996082db1f2f2c32af060d7aa15c2d'
        self.targetDigests['2.1.0'] = 'b08197d146930a5543a7b99e871cba3da614f6f0'
        self.shortDescription = "XML parser library written in C"
        self.defaultTarget = '2.1.0'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        # both examples and tests can be run here
        self.subinfo.options.configure.defines = "-DBUILD_tests=OFF -DBUILD_examples=OFF -DBUILD_tools=OFF"
        self.subinfo.options.configure.testDefine = "-DBUILD_tests=ON  -DBUILD_examples=ON"
        self.subinfo.options.configure.toolsDefine = "-DBUILD_tools=ON" # available only from 2.1.0-beta3
        self.subinfo.options.configure.staticDefine = "-DBUILD_shared=OFF" # available only from 2.1.0-beta3

    def createPackage( self ):
        libName="libexpat"
        self.stripLibs( libName )
        return KDEWinPackager.createPackage( self )

if __name__ == '__main__':
     Package().execute()
