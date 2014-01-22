import info

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['2.2.0', '2.2.3', '2.3.1', '2.3.2']:
            self.targets[ ver ] = 'http://downloads.sourceforge.net/sourceforge/openbabel/openbabel-' + ver + '.tar.gz'
            self.targetInstSrc[ ver ] = 'openbabel-' + ver
        self.patchToApply['2.2.0'] = ('openbabel-2.2.0-cmake.diff', 0)
        self.patchToApply['2.2.3'] = ('openbabel-2.2.3-20101208.diff', 1)
        self.patchToApply['2.3.1'] = [('openbabel-2.3.1-20130430.diff', 1)]
        self.patchToApply['2.3.2'] = [('openbabel-2.3.2-20131003.diff', 1)]
        self.targetDigests['2.3.1'] = 'b2dd1638eaf7e6d350110b1561aeb23b03552846'
        self.targetDigests['2.3.2'] = 'b8831a308617d1c78a790479523e43524f07d50d'

        self.shortDescription = "library to convert the various file formats used in chemical software"
        self.defaultTarget = '2.3.2'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['win32libs/boost-headers'] = 'default'
        self.dependencies['win32libs/zlib'] = 'default'
        self.dependencies['win32libs/libxml2'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self, **args):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
