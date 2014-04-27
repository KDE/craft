# -*- coding: utf-8 -*-
import info
import compiler

#TODO: find a clean solution to run it with msvc support(lib.exe must be in path to generate msvc import libs)

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = "git://git.videolan.org/ffmpeg.git"
        for ver in ["0.8.6", "0.11.2",  "1.1.3", "2.0.1"]:
                self.targets[ ver ] = "http://ffmpeg.org/releases/ffmpeg-%s.tar.bz2" % ver 
                self.targetInstSrc[ ver ] = "ffmpeg-%s" % ver
        self.targetDigests['0.8.6'] = 'ad7eaefa5072ca3c11778f9186fab35558a04478'
        self.targetDigests['0.11.2'] = '5d98729b8368df8145472ae6955ef8d6b9ed0efb'
        self.targetDigests['1.1.3'] = 'd82d6f53c5130ee21dcb87f76bdbdf768d3f0db9'
        
        self.defaultTarget = "2.0.1"


    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        if compiler.isMinGW():
            self.buildDependencies['dev-util/msys'] = 'default'
            self.buildDependencies['dev-util/yasm'] = 'default'
        self.dependencies['win32libs/libvorbis'] = 'default'
        self.dependencies['win32libs/liblame'] = 'default'
        self.dependencies['win32libs/libopus'] = 'default'


from Package.AutoToolsPackageBase import *
from Package.VirtualPackageBase import *

class PackageMinGW(AutoToolsPackageBase):
    def __init__( self, **args ):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.package.withCompiler = False
        self.platform = ""
        self.subinfo.options.configure.defines = " --disable-static --enable-shared --enable-gpl --enable-libvorbis  --disable-doc  --enable-libmp3lame --enable-libopus --enable-w32threads"
        
    def configure( self):
        return AutoToolsPackageBase.configure( self, cflags="-std=c99 ", ldflags="")
        
    def ccacheOptions(self):
        return " --cc='ccache gcc' --cxx='ccache g++' "


if compiler.isMinGW():
    class Package(PackageMinGW):
        def __init__( self ):
            PackageMinGW.__init__( self )
else:
    class Package(VirtualPackageBase):
        def __init__( self ):
            VirtualPackageBase.__init__( self )

if __name__ == '__main__':
      Package().execute()
