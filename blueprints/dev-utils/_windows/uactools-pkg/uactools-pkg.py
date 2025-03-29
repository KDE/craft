import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.compiler = CraftCore.compiler.Compiler.GCCLike

    def setDependencies(self):
        # This Package provides the binaries for uactools-bin but virtual/base can
        # not depend on it because it needs a compiler itself.
        self.runtimeDependencies["virtual/base"] = None

    def setTargets(self):
        self.svnTargets["svnHEAD"] = "trunk/kdesupport/kdewin/tools/mt"
        self.defaultTarget = "svnHEAD"


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DCMAKE_EXE_LINKER_FLAGS=-static"]
