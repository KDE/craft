# -*- coding: utf-8 -*-
import os

import info
import compiler


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['5.0.2'] = "ftp://ftp.gmplib.org/pub/gmp-5.0.2/gmp-5.0.2.tar.bz2"
        self.targetDigests['5.0.2'] = '2968220e1988eabb61f921d11e5d2db5431e0a35'
        self.targetInstSrc['5.0.2'] = "gmp-5.0.2"
        self.defaultTarget = '5.0.2'


    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['dev-util/msys'] = 'default'


from Package.AutoToolsPackageBase import *
from Package.VirtualPackageBase import *

class PackageMinGW(AutoToolsPackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.package.withCompiler = False
        self.subinfo.options.configure.defines = "--disable-static --enable-shared --enable-cxx "
        self.buildInSource = True
        
    def configure( self):
        return AutoToolsPackageBase.configure( self, cflags="-std=c99 ", ldflags="")
        

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

    