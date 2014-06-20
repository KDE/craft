# -*- coding: utf-8 -*-
import info
import utils
import compiler
import shutil
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in [ '1.2.5', '1.2.6', '1.2.7', '1.2.8' ]:
            self.targets[ ver ] = 'http://downloads.sourceforge.net/sourceforge/libpng/zlib-%s.tar.gz' % ver
            self.targetInstSrc[ ver ] = "zlib-" + ver
        self.patchToApply['1.2.5'] = [("zlib-1.2.5-20110629.diff", 1)]
        self.patchToApply['1.2.6'] = [("zlib-1.2.6-20120421.diff", 1)]
        self.patchToApply['1.2.7'] = [("zlib-1.2.7-20130123.diff", 1)]
        self.patchToApply['1.2.8'] = [("zlib-1.2.8-20130901.diff", 1)]
        self.targetDigests['1.2.5'] = '8e8b93fa5eb80df1afe5422309dca42964562d7e'
        self.targetDigests['1.2.7'] = '4aa358a95d1e5774603e6fa149c926a80df43559'
        self.targetDigests['1.2.8'] = 'a4d316c404ff54ca545ea71a27af7dbc29817088'

        self.shortDescription = 'The zlib compression and decompression library'
        self.defaultTarget = '1.2.8'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        if emergePlatform.isCrossCompilingEnabled():
            self.dependencies['win32libs/wcecompat'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
