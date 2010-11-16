# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['0.9', '0.9.3']:
            self.targets[ ver ] = "http://www.nih.at/libzip/libzip-" + ver + ".tar.bz2"
            self.targetInstSrc[ ver ] = "libzip-" + ver
        self.patchToApply['0.9.0'] = ( 'libzip-0.9.diff', 1 )
        self.patchToApply['0.9.3'] = ( 'libzip-0.9.3-20101116.diff', 1 )
        self.targetDigests['0.9.3'] = '16e94bc0327f1a76a0296a28908cf6439b0a0a67'
        self.defaultTarget = '0.9.3'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs-bin/zlib'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()