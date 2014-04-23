# -*- coding: utf-8 -*-
import info
import compiler


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['3.99.5'] = "http://downloads.sourceforge.net/sourceforge/lame/lame-3.99.5.tar.gz"
        self.targetDigests['3.99.5'] = '03a0bfa85713adcc6b3383c12e2cc68a9cfbf4c4'
        self.targetInstSrc['3.99.5'] = "lame-3.99.5"
        self.defaultTarget = '3.99.5'


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
        self.subinfo.options.configure.defines = "--disable-static --enable-shared " 


        

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
