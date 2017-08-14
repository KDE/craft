import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/uclouvain/openjpeg.git"

        for ver in ["2.1.2"]:
            self.targets[ver] = f"https://github.com/uclouvain/openjpeg/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"openjpeg-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"openjpeg-{ver}"
        self.targetDigests['2.1.2'] = (
            ['4ce77b6ef538ef090d9bde1d5eeff8b3069ab56c4906f083475517c2c023dfa7'], CraftHash.HashAlgorithm.SHA256)

        self.description = "OpenJPEG is an open-source JPEG 2000 codec written in C language."
        self.webpage = "http://www.openjpeg.org/"
        self.defaultTarget = "2.1.2"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
