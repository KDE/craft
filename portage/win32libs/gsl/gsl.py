import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = "[git]https://github.com/ampl/gsl.git"
        for ver in ["2.2.1"]:
            self.targets[ver] = f"https://github.com/ampl/gsl/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"gsl-{ver}"
            self.archiveNames[ver] = f"gsl-{ver}.tar.gz"
        self.targetDigests['2.2.1'] = (
            ['ca58c082a925efe83a30ae4b9882511aee5937f6e6db17e43365a60e29a0a52e'], CraftHash.HashAlgorithm.SHA256)
        self.description = 'GNU Scientific Library'
        self.patchToApply['2.2.1'] = [("disable-broken-pdb-install.patch", 1)]
        self.defaultTarget = '2.2.1'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
