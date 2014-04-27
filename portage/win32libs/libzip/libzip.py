# -*- coding: utf-8 -*-
import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ['0.9', '0.9.3']:
            self.targets[ ver ] = "http://www.nih.at/libzip/libzip-" + ver + ".tar.bz2"
            self.targetInstSrc[ ver ] = "libzip-" + ver
        for ver in ['0.11.1']:
            self.targets[ ver ] = "http://www.nih.at/libzip/libzip-" + ver + ".tar.xz"
            self.targetInstSrc[ ver ] = "libzip-" + ver
        self.patchToApply['0.9.0'] = ( 'libzip-0.9.diff', 1 )
        self.patchToApply['0.9.3'] = ( 'libzip-0.9.3-20101116.diff', 1 )
        self.patchToApply['0.11.1'] = ( 'libzip-0.11.1-20130907.diff', 1 )
        self.targetDigests['0.9.3'] = '16e94bc0327f1a76a0296a28908cf6439b0a0a67'
        self.targetDigests['0.11.1'] = '3c82cdc0de51f06d5e1c60f098d3d9cc0d48f8a7'

        self.shortDescription = "a library for handling zip archives"
        self.defaultTarget = '0.11.1'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs/zlib'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()