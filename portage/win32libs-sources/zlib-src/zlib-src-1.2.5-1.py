# -*- coding: utf-8 -*-
import info
import utils
import compiler
import shutil
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
       for ver in [ '1.2.5' ]:
           self.targets[ ver ] = 'http://downloads.sourceforge.net/sourceforge/libpng/zlib-%s.tar.gz' % ver
           self.targetInstSrc[ ver ] = "zlib-" + ver
       self.patchToApply['1.2.5'] = ("zlib-1.2.5-20110629.diff", 1)
       self.targetDigests['1.2.5'] = '8e8b93fa5eb80df1afe5422309dca42964562d7e'

       self.shortDescription = 'The zlib compression and decompression library'
       self.defaultTarget = '1.2.5'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        if emergePlatform.isCrossCompilingEnabled():
            self.dependencies['win32libs-sources/wcecompat-src'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.staticDefine = "-DBUILD_SHARED_LIBS=OFF"
        
    def install(self):
        if not CMakePackageBase.install(self):
            return False
        #to stay compatible to previous builds
        if compiler.isMinGW() and not utils.varAsBool(self.subinfo.options.buildStatic):
            shutil.copy(os.path.join( self.installDir() , "bin","libz.dll"),os.path.join( self.installDir() , "bin","libzlib1.dll"))
        return True

if __name__ == '__main__':
    Package().execute()
