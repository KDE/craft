import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['0.7.3'] = 'http://code.compeng.uni-frankfurt.de/attachments/download/174/Vc-0.7.3.tar.gz'
        self.targetDigests['0.7.3'] = 'aa41aeddac59abc60f292de8fdedbe70a4b49108'
        self.targetInstSrc['0.7.3'] = "Vc-0.7.3"
        self.patchToApply['0.7.3'] = ("Vc-0.7.3-20140107.diff", 1)

        # Note: at the moment Vc does not provide a stable MSVC-compatible release.
        # Please update the default target to a tarball once one is made available.
        self.svnTargets['0.7'] = 'https://github.com/VcDevel/Vc.git|0.7'
        self.description = 'Portable, zero-overhead SIMD library for C++'
        self.defaultTarget = '0.7.3'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

        self.subinfo.options.configure.args = " -DBUILD_TESTING=OFF "
        if craftCompiler.isMSVC():
            self.subinfo.options.configure.args += " -DCMAKE_CXX_FLAGS=/FS "
