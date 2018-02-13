# -*- coding: utf-8 -*-

import info
from Package.MaybeVirtualPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        ver = "2.16.1"
        build = "4"
        self.targets[ver] = f"https://github.com/git-for-windows/git/releases/download/v{ver}.windows.{build}/PortableGit-{ver}.{build}-{CraftCore.compiler.bits}-bit.7z.exe"
        self.archiveNames[ver] = f"PortableGit-{ver}-{CraftCore.compiler.bits}-bit.7z"
        self.targetInstallPath[ver] = os.path.join("dev-utils", "git")
        self.targetDigests[ver] = (["5d3e89163cb8b88484d906f8ba53604279e3d7b8c170e39d89116aa5c7274f26"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigestsX64[ver] = (['a2191f676d77f8b8ba88501b8d373dc5418845c52dca86313ec449881af14cbd'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = ver

    def setDependencies(self):
        self.buildDependencies["dev-util/7zip"] = "default"
        self.buildDependencies["gnuwin32/wget"] = "default"
        self.buildDependencies["dev-util/shimgen"] = "default"


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
        utils.system([os.path.join(gitDir, "git-cmd.exe"), "--no-cd", "--command=post-install.bat"], cwd=gitDir)
        return True


class Package(VirtualIfSufficientVersion):
    def __init__(self):
        VirtualIfSufficientVersion.__init__(self, app="git", version="2.13.0", classA=GitPackage)
