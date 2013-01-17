# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets[ '3.0.10rc8' ] = "ftp://sources.redhat.com/pub/libffi/libffi-3.0.10rc8.tar.gz"
        self.targetInstSrc[ '3.0.10rc8' ] = "libffi-3.0.10rc8"
        self.targetDigests['3.0.10rc8'] = '1dc449254c4c8bde1f422955e378016ba748d3f2'
        self.patchToApply['3.0.10rc8'] = [("libffi-3.0.10rc8-20110722.diff", 1)]
        self.shortDescription = "a foreign function interface library"
        self.defaultTarget = '3.0.10rc8'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'


class PackageMSVC(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

from Package.AutoToolsPackageBase import *

class PackageMinGW( AutoToolsPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        AutoToolsPackageBase.__init__(self)
        if os.getenv("EMERGE_ARCHITECTURE") == "x64":
            target = "x86_64-w64-mingw32"
        else:
            target = "i686-w64-mingw32"
        self.subinfo.options.configure.defines = " --enable-static=no --enable-shared=yes --host=%s" % target 
        
        
if compiler.isMinGW():
    class Package(PackageMinGW):
        def __init__( self ):
            PackageMinGW.__init__( self )
else:
    class Package(PackageMSVC):
        def __init__( self ):
            self.subinfo = subinfo()
            PackageMSVC.__init__( self )

if __name__ == '__main__':
      Package().execute()