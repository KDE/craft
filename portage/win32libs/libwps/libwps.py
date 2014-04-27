import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['0.2.4']:
            self.targets[ ver ] = "http://download.sourceforge.net/libwps/libwps-" + ver + ".tar.bz2"
            self.targetInstSrc[ ver ] = "libwps-" + ver
        self.patchToApply['0.2.4'] = ( 'libwps-0.2.4-cmake.diff', 1 )
        self.targetDigests['0.2.4'] = '9fff59d92d9f34259ea5b1d9eca5c30313453a64'

        self.shortDescription = "A library to read and parse Microsoft Works format"
        self.defaultTarget = '0.2.4'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs/libwpd'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )

