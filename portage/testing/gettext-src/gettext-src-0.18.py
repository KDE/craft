# -*- coding: utf-8 -*-
import info
import utils
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
       self.targets[ '0.18' ] = 'http://ftp.gnu.org/pub/gnu/gettext/gettext-0.18.tar.gz'
       self.targetInstSrc[ '0.18' ] = "gettext-0.18"
       self.patchToApply['0.18'] = ("gettext-0.18-20100521.diff", 1)
       self.defaultTarget = '0.18'

    def setDependencies( self ):
        self.hardDependencies['dev-util/cmake'] = 'default'
        self.hardDependencies['win32libs-sources/win_iconv-src'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
