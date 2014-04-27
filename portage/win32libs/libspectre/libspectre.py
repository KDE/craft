import info

class subinfo(info.infoclass):
    def setTargets( self ):
        """ """
        for ver in ['0.2.1', '0.2.6', '0.2.7']:
            self.targets[ver] = "http://libspectre.freedesktop.org/releases/libspectre-" + ver + ".tar.gz"
            self.targetInstSrc[ver] = "libspectre-" + ver
        self.patchToApply["0.2.1"] = ("spectre-0.2.1-cmake.diff", 1)
        self.patchToApply["0.2.6"] = ("libspectre-0.2.6-20101117.diff", 1)
        self.patchToApply["0.2.7"] = ("libspectre-0.2.7-20131003.diff", 1)
        self.targetDigests['0.2.6'] = '819475c7e34a1e9bc2e876110fee530b42aecabd'
        self.targetDigests['0.2.7'] = 'a7efd97b82b84ff1bb7a0d88c7e35ad10cc84ea8'

        self.shortDescription = "a wrapper library for libgs"
        self.defaultTarget = '0.2.7'

    def setDependencies( self ):
        self.dependencies['binary/ghostscript'] = 'default'
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
