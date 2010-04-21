# -*- coding: utf-8 -*-
import info
import utils
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
       for ver in [ '1.2.4' ]:
           self.targets[ ver ] = 'http://downloads.sourceforge.net/sourceforge/libpng/zlib-%s.tar.gz' % ver
           self.targetInstSrc[ ver ] = "zlib-" + ver
       self.patchToApply['1.2.4'] = ("zlib-1.2.4-20100329.diff", 1)
       self.defaultTarget = '1.2.4'

    def setDependencies( self ):
        self.hardDependencies['dev-util/cmake'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        self.subinfo.options.package.withCompiler = None
        CMakePackageBase.__init__( self )

    def unpack(self):
        if not CMakePackageBase.unpack( self ):
            return False       
        if os.path.exists(os.path.join( self.sourceDir() , "zconf.h" )):
            os.remove(os.path.join( self.sourceDir() , "zconf.h" ))
        return True
        
    def make(self, unused=''):        
        if self.isTargetBuild():
           # This is needed to find some wcecompat files (e.g. errno.h) included by some openssl headers
           # but we make sure to add it at the very end so it doesn't disrupt the rest of the Qt build
           os.environ["TARGET_INCLUDE"] = os.getenv("TARGET_INCLUDE") + ";" + os.path.join( self.mergeDestinationDir(), "include", "wcecompat" )

        CMakeBuildSystem.make(self)
        
        return True

    def createPackage( self ):
        # auto-create both import libs with the help of pexports
        self.createImportLibs( "zlib1" )

        return CMakePackageBase.createPackage( self )

if __name__ == '__main__':
    Package().execute()
