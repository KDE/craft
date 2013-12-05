# -*- coding: utf-8 -*-
import info
import os
import compiler
import shells

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.0.3'] = "http://downloads.xiph.org/releases/opus/opus-1.0.3.tar.gz"
        self.targetDigests['1.0.3'] = '5781bdd009943deb55a742ac99db20a0d4e89c1e'
        self.targetInstSrc['1.0.3'] = "opus-1.0.3"

        self.shortDescription = "Opus codec library"
        self.defaultTarget = '1.0.3'

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
        self.shell = MSysShell()
        self.subinfo.options.configure.defines = "--disable-static --enable-shared --disable-doc" 


        

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
