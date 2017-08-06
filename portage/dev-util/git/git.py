# -*- coding: utf-8 -*-

import info
from Package.MaybeVirtualPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        ver = "2.11.0"
        arch = 32
        if craftCompiler.isX64():
            arch = 64

        self.targets[
            ver] = "https://github.com/git-for-windows/git/releases/download/v%s.windows.1/PortableGit-%s-%s-bit.7z.exe" % (
        ver, ver, arch)
        self.archiveNames[ver] = "PortableGit-%s-%s-bit.7z" % (ver, arch)
        self.targetInstallPath[ver] = os.path.join("dev-utils", "git")
        self.defaultTarget = ver

    def setDependencies(self):
        self.buildDependencies["virtual/bin-base"] = "default"


from Package.BinaryPackageBase import *


class GitPackage(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def install(self):
        if not BinaryPackageBase.install(self):
            return False
        utils.createShim(os.path.join(self.imageDir(), "dev-utils", "bin", "git.exe"),
                         os.path.join(self.imageDir(), "dev-utils", "git", "bin", "git.exe"))
        return True

    def qmerge(self):
        if not BinaryPackageBase.qmerge(self):
            return False
        gitDir = os.path.join(CraftStandardDirs.craftRoot(), "dev-utils", "git")
        utils.system(os.path.join(gitDir, "post-install.bat"), cwd=gitDir)
        return True


class Package(VirtualIfSufficientVersion):
    def __init__(self):
        VirtualIfSufficientVersion.__init__(self, app="git", version="2.10.0", classA=GitPackage)
