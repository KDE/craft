# -*- coding: utf-8 -*-
import info
import utils
import compiler
import shutil
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in [ '1.2.5', '1.2.6' ]:
            self.targets[ ver ] = 'http://downloads.sourceforge.net/sourceforge/libpng/zlib-%s.tar.gz' % ver
            self.targetInstSrc[ ver ] = "zlib-" + ver
        self.patchToApply['1.2.5'] = [("zlib-1.2.5-20110629.diff", 1)]
        self.patchToApply['1.2.6'] = [("zlib-1.2.6-20120421.diff", 1)]
        self.targetDigests['1.2.5'] = '8e8b93fa5eb80df1afe5422309dca42964562d7e'

        self.shortDescription = 'The zlib compression and decompression library'
        self.defaultTarget = '1.2.6'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        if emergePlatform.isCrossCompilingEnabled():
            self.dependencies['win32libs/wcecompat-src'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.staticDefine = "-DBUILD_SHARED_LIBS=OFF"

if __name__ == '__main__':
    Package().execute()
