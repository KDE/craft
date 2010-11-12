import os
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        self.targets['2.0.1'] = 'http://downloads.sourceforge.net/sourceforge/expat/expat-2.0.1.tar.gz'
        self.targetInstSrc['2.0.1'] = 'expat-2.0.1'
        self.patchToApply['2.0.1'] = ('expat-2.0.1-20100329.diff', 1)
        self.targetDigests['2.0.1'] = '663548c37b996082db1f2f2c32af060d7aa15c2d'
        self.defaultTarget = '2.0.1'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        # both examples and tests can be run here
        self.subinfo.options.configure.defines = "-DBUILD_tests=OFF -DBUILD_examples=OFF"
        
    def createPackage( self ):
        libName="libexpat" 
        self.stripLibs( libName )
        return KDEWinPackager.createPackage( self )
           
if __name__ == '__main__':
     Package().execute()
