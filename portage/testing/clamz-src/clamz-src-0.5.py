# -*- coding: utf-8 -*-
import info
import os
import compiler

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.5'] = "http://clamz.googlecode.com/files/clamz-0.5.tar.gz"
        self.targetDigests['0.5'] = '54664614e5098f9e4e9240086745b94fe638b176'
        self.targetInstSrc['0.5'] = "clamz-0.5"
        self.patchToApply['0.5'] = [("clamz-0.5-20120913.diff",1)]
        
        self.defaultTarget = '0.5'


    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        if compiler.isMinGW():
            self.buildDependencies['dev-util/msys'] = 'default'
            self.dependencies['testing/gcrypt'] = 'default'
            self.dependencies['kdesupport/kdewin'] = 'default'
            self.dependencies['win32libs/libcurl'] = 'default'


from Package.AutoToolsPackageBase import *
from Package.VirtualPackageBase import *

class PackageMinGW(AutoToolsPackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.defines = " LIBCURL_CFLAGS='-I.'  LIBCURL_LIBS=-lcurl LIBGCRYPT_LIBS='-lgcrypt -lkdewin'  LIBGCRYPT_CFLAGS='-I.' "
        
    def configure(self):
      return AutoToolsPackageBase.configure( self,cflags = " -I/r/include/mingw/ ")

if compiler.isMinGW():
    class Package(PackageMinGW):
        def __init__( self ):
            PackageMinGW.__init__( self )
else:
    class Package(VirtualPackageBase):
        def __init__( self ):
            self.subinfo = subinfo()
            VirtualPackageBase.__init__( self )

if __name__ == '__main__':
      Package().execute()
