# -*- coding: utf-8 -*-
import base
import os
import shutil
import utils
import info

import compiler

class subinfo(info.infoclass):
    def setTargets( self ):
        ver = '5.0.0'
        self.targets[ver] = 'http://tukaani.org/xz/xz-' + ver + '.tar.xz'
        self.targetInstSrc[ver] = 'xz-' + ver
        self.patchToApply[ver] = ('xz-5.0.0-20101205.diff',1)
        self.targetDigests['5.0.0'] = '73ca893ab1ece362d35445145a37cefd0a95310b'
        
        self.shortDescription = "free general-purpose data compression software with high compression ratio"
        self.defaultTarget = ver
        
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'


from Package.CMakePackageBase import *
from Package.VirtualPackageBase import *
 
class PackageMinGW( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.package.withCompiler = False

    def createPackage( self ):        
        shutil.copy( os.path.join( self.imageDir() , "lib" ,"liblzma.dll.a" ) , os.path.join( self.imageDir() , "lib" ,"liblzma.lib" ))
        return KDEWinPackager.createPackage( self )

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