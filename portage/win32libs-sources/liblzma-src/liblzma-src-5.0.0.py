# -*- coding: utf-8 -*-
import base
import os
import shutil
import utils
import info

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
        
class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

    def make_package( self ):
        self.createImportLibs( "liblzma" )
        return True

if __name__ == '__main__':
    Package().execute()