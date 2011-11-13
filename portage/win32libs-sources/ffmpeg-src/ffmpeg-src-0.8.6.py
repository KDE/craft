# -*- coding: utf-8 -*-
import info
import os
import compiler

#TODO: find a clean solution to run it with msvc support(lib.exe must be in path to generate msvc import libs)

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = "git://git.videolan.org/ffmpeg.git"
        self.targets['0.8.6'] = "http://ffmpeg.org/releases/ffmpeg-0.8.6.tar.bz2"
        self.targetInstSrc['0.8.6'] = "ffmpeg-0.8.6"
        self.targetDigests['0.8.6'] = 'ad7eaefa5072ca3c11778f9186fab35558a04478'
        self.defaultTarget = '0.8.6'


    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['dev-util/autotools'] = 'default'
        self.buildDependencies['dev-util/yasm'] = 'default'


from Package.AutoToolsPackageBase import *
from Package.VirtualPackageBase import *

class PackageMinGW(AutoToolsPackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.package.withCompiler = False
        self.subinfo.options.configure.defines = " --enable-memalign-hack --disable-static --enable-shared --enable-gpl"
        
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
