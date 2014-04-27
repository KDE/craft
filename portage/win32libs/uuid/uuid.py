import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.6.2'] = 'http://downloads.sourceforge.net/kde-windows/uuid-1.6.2.tar.gz'
        self.patchToApply['1.6.2'] = [('uuid-cmake.diff', 1)]
        self.targetInstSrc['1.6.2'] = 'uuid-1.6.2'
        self.targetDigests['1.6.2'] = '3e22126f0842073f4ea6a50b1f59dcb9d094719f'
        self.shortDescription = "OSSP uuid is a library and cli for the generation of multi standard compliant Universally Unique Identifier (UUID)."
        self.defaultTarget = '1.6.2'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

        # building dce and c++ interface not needed
        self.subinfo.options.configure.defines = "-DWITH_DCE=OFF -DWITH_CXX=OFF -DWITH_EXEC=OFF"

