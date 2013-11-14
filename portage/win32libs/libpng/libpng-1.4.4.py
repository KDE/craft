import shutil
import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['1.4.4','1.2.43', '1.5.14', '1.6.6']:
            self.targets[ver] = 'http://downloads.sourceforge.net/libpng/libpng-' + ver + '.tar.gz'
            self.targetInstSrc[ver] = 'libpng-' + ver
        # patch is only required for wince, update if necessary
        self.patchToApply['1.4.4'] = ("libpng-1.4.4-20100517.diff", 1)
        self.targetDigests['1.4.4'] = '245490b22086a6aff8964b7d32383a17814d8ebf'
        self.targetDigests['1.5.14'] = '67f20d69564a4a50204cb924deab029f11ad2d3c'
        self.targetDigests['1.6.6'] = '609c355beef7c16ec85c4580eabd62efe75383af'

        self.shortDescription = 'A library to display png images'
        self.defaultTarget = '1.6.6'

    def setDependencies( self ):
        self.dependencies['win32libs/zlib'] = 'default'
        self.buildDependencies['virtual/base'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DPNG_TESTS=OFF -DPNG_STATIC=OFF -DPNG_NO_STDIO=OFF"
        self.subinfo.options.package.packageName = 'libpng'

if __name__ == '__main__':
    Package().execute()

