# -*- coding: utf-8 -*-
import info
import os
import compiler
import shells

#TODO: find a clean solution to run it with msvc support(lib.exe must be in path to generate msvc import libs)

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['3.98.4'] = "http://downloads.sourceforge.net/sourceforge/lame/lame-3.98.4.tar.gz"
        #self.targetDigests['3.99.3'] = '0d9acaed7737d5e6b51096dc0b35322d319f463d'
        self.targetInstSrc['3.98.4'] = "lame-3.98.4"
        self.defaultTarget = '3.98.4'


    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['dev-util/autotools'] = 'default'


from Package.AutoToolsPackageBase import *
from Package.VirtualPackageBase import *

class PackageMinGW(AutoToolsPackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.package.withCompiler = False
        self.shell = MSysShell()
        self.subinfo.options.configure.defines = "--disable-static --enable-shared --enable-nasm" 


        

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
