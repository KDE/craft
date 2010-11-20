import base
import os
import sys
import shutil
import utils
import info


class subinfo(info.infoclass):
    def setTargets( self ):
      for ver in ( '1.12', '1.13', '1.13.1' ):
        self.targets[ver]       = 'http://ftp.gnu.org/pub/gnu/libiconv/libiconv-%s.tar.gz' % ver
        self.targetInstSrc[ver] = 'libiconv-%s' % ver
        self.patchToApply[ver]  = ( 'iconv-src-%s.patch' % ver, 0 )

      self.targetDigests['1.13.1'] = '5b0524131cf0d7abd50734077f13aaa5508f6bbe'
      self.defaultTarget = '1.13.1'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['dev-util/msys'] = 'default'

from Package.AutoToolsPackageBase import *

class Package(AutoToolsPackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        self.subinfo.options.package.packageName = 'iconv'
        AutoToolsPackageBase.__init__(self)        
        
    def install( self ):
        if not AutoToolsPackageBase.install( self ):
            return False
        ## @todo move to AutoToolsPackageBase::install
        utils.fixCmakeImageDir( self.installDir(), self.mergeDestinationDir().replace(":","\\" ) )

        # do not create msvc import libs in x64 mode
        if self.buildArchitecture() == "x64":
            return True
            
        for libs in "libiconv-2 libcharset-1".split():
            if not self.createImportLibs( libs ):
                return False;
        return True

if __name__ == '__main__':
    Package().execute()
