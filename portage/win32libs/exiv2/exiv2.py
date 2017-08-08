import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['0.24', '0.25']:
            self.targets[ver] = 'http://www.exiv2.org/exiv2-%s.tar.gz' % ver
            self.targetInstSrc[ver] = 'exiv2-%s' % ver
        self.targetDigests['0.24'] = '2f19538e54f8c21c180fa96d17677b7cff7dc1bb'
        self.patchToApply['0.24'] = ('exiv2-0.22-20120117.diff', 1)
        self.patchToApply['0.25'] = ('exiv2-0.25-20150826.diff', 1)
        self.targetDigests['0.25'] = 'adb8ffe63916e7c27bda9792e690d1330ec7273d'

        self.svnTargets['svnHEAD'] = 'svn://dev.exiv2.org/svn/trunk'

        self.description = "an image metadata library"
        self.defaultTarget = '0.25'

    def setDependencies(self):
        self.runtimeDependencies["win32libs/win_iconv"] = "default"
        self.runtimeDependencies["win32libs/gettext"] = "default"
        self.runtimeDependencies["win32libs/expat"] = "default"
        self.runtimeDependencies["win32libs/zlib"] = "default"
        self.runtimeDependencies["virtual/base"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.supportsNinja = False
        self.subinfo.options.configure.args = "-DEXIV2_ENABLE_BUILD_SAMPLES=OFF"
