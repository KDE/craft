# -*- coding: utf-8 -*-
import os

import info
import compiler


#TODO: find a clean solution to run it with msvc support(lib.exe must be in path to generate msvc import libs)

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.9.3'] = "http://musicip-libofa.googlecode.com/files/libofa-0.9.3.tar.gz"
        self.targetInstSrc['0.9.3'] = "libofa-0.9.3"
        self.patchToApply[ '0.9.3' ] = [ ( 'libofa-0.9.3-20111221.diff', 1 ) ]        
        self.targetDigests['0.9.3'] = '3dec8e1dcea937f74b4165e9ffd4d4f355e4594a'
        self.defaultTarget = '0.9.3'


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
        self.subinfo.options.configure.defines = "--disable-static --enable-shared CPPFLAGS=-I%s " % self.shell.toNativePath(os.path.join(os.getenv("KDEROOT"),"include")) 


        

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
