import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['0.17.2'] = ["http://www.libraw.org/data/LibRaw-0.17.2.tar.gz",
                                  "https://github.com/LibRaw/LibRaw-cmake/archive/master.zip"]
        self.archiveNames['0.17.2'] = ["LibRaw-0.17.2.tar.gz",
                                       "LibRaw-0.17.2-cmake.zip"]
        self.targetInstSrc['0.17.2'] = "LibRaw-0.17.2"
        self.description = "LibRaw is a library for reading RAW files obtained from digital photo cameras (CRW/CR2, NEF, RAF, DNG, and others)."
        self.targetDigests['0.17.2'] = (
            ['92b0c42c7666eca9307e5e1f97d6fefc196cf0b7ee089e22880259a76fafd15c'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '0.17.2'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["win32libs/jasper"] = "default"
        self.runtimeDependencies["win32libs/lcms"] = "default"
        self.runtimeDependencies["win32libs/libjpeg-turbo"] = "default"


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def unpack(self):
        if not CMakePackageBase.unpack(self):
            return False
        utils.mergeTree(os.path.join(self.workDir(), "LibRaw-cmake-master"),
                        self.sourceDir())
        return True
