import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs/openssl'] = 'default'
        self.dependencies['win32libs/zlib'] = 'default'
        self.dependencies['win32libs/libidn'] = 'default'

    def setTargets( self ):
        for ver in ['1.0', '1.0.13']:
            self.targets[ ver ] = "http://camaya.net/download/gloox-" + ver + ".tar.bz2"
            self.targetInstSrc[ ver ] = "gloox-" + ver
        self.patchToApply['1.0'] = [('gloox-1.0-20101111.diff', 1)]
        self.patchToApply['1.0.13'] = [('gloox-1.0.13-20150408.diff', 1)]

        self.targetDigests['1.0'] = '8c788738f72b05fae7c05c744a67859419ffa09c'
        self.targetDigests['1.0.13'] = '735c0507f4ac45e6990528fab6afc45f9cabcc3a'

        self.defaultTarget = '1.0.13'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )

