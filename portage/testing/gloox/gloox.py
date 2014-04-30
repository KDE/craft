import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.dependencies['virtual/base'] = 'default'
        self.dependencies['win32libs/openssl'] = 'default'
        self.dependencies['win32libs/zlib'] = 'default'
        self.dependencies['win32libs/libidn'] = 'default'

    def setTargets( self ):
        for ver in ['1.0']:
            self.targets[ ver ] = "http://camaya.net/download/gloox-" + ver + ".tar.bz2"
            self.targetInstSrc[ ver ] = "gloox-" + ver
        self.patchToApply['1.0'] = [('gloox-1.0-20101111.diff', 1)]

        self.targetDigests['1.0'] = '8c788738f72b05fae7c05c744a67859419ffa09c'

        self.defaultTarget = '1.0'
        self.options.configure.defines = ""

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )

