import os
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.defaultTarget = '0.2.6'
        self.shortDescription = "a library to perform image correction based on lens profiles"
        
        for ver in ['0.2.6']:
            self.targets[ver] = "http://sourceforge.net/projects/lensfun.berlios/files/lensfun-%s.tar.bz2/download/lensfun-%s.tar.bz2" % (ver, ver)
            self.targetInstSrc[ver] = "lensfun-%s" % ver
        
        self.targetDigests['0.2.6'] = '0d7ffbae5c54159308114f69a9e2bc5f4d24d836'
        
        self.patchToApply['0.2.6'] = ( 'lensfun-0.2.6.diff', 1 )
        
    
    def setBuildOptions( self ):
        info.infoclass.setBuildOptions(self)
        
        self.options.configure.defines = "-DBUILD_STATIC=OFF"
        self.options.configure.defines += " -DBUILD_TESTS=OFF"
        self.options.configure.defines += " -DBUILD_AUXFUN=OFF"
        self.options.configure.defines += " -DBUILD_FOR_SSE=ON"
        self.options.configure.defines += " -DBUILD_FOR_SSE2=ON"
        self.options.configure.defines += " -DBUILD_DOC=OFF"
        
    
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        # self.buildDependencies['dev-util/doxygen'] = 'default' # only needed if building docs
        self.dependencies['testing/glib-src'] = 'default'
        # self.dependencies['win32libs-bin/zlib']  = 'default' # only needed if building auxfun and tests
        # self.dependencies['win32libs-bin/libpng'] = 'default' # only needed if building auxfun and tests
        

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
