# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets[ '3.0.10' ] = "ftp://sources.redhat.com/pub/libffi/libffi-3.0.10.tar.gz"
        self.targetInstSrc[ '3.0.10' ] = "libffi-3.0.10"
        self.targetDigests['3.0.10'] = '97abf70e6a6d315d9259d58ac463663051d471e1'
        self.patchToApply['3.0.10'] = [("libffi-3.0.10rc8-20110722.diff", 1)]
        self.shortDescription = "a foreign function interface library"
        self.defaultTarget = '3.0.10'

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
        self.subinfo.options.configure.defines = " --disable-static --enable-shared "
        
        
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