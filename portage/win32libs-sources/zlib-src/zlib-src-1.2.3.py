# -*- coding: utf-8 -*-
import info
import utils
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets[ '1.2.3-3' ] = 'http://www.zlib.net/zlib-1.2.3.tar.gz'
        self.targets[ '1.2.4' ] = 'http://zlib.net/zlib-1.2.4.tar.gz'
        self.defaultTarget = '1.2.4'

    def setDependencies( self ):
        self.hardDependencies['dev-util/cmake'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        self.subinfo.options.package.withCompiler = None
        CMakePackageBase.__init__( self )

    def buildType( self ):
        return "Release"
  
    def unpack(self):
        if not CMakePackageBase.unpack( self ):
            return False
        # copy CMakeLists.txt
        utils.copyFile( os.path.join( self.packageDir(), "CMakeLists.txt" ),
                        os.path.join( self.sourceDir(),  "CMakeLists.txt" ) )
        return True

    def createPackage( self ):
        # auto-create both import libs with the help of pexports
        self.createImportLibs( "zlib" )

        return CMakePackageBase.createPackage( self )

if __name__ == '__main__':
    Package().execute()
