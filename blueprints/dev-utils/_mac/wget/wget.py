import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.21.2-18"]:
            self.targets[ver] = f"https://files.kde.org/craft/prebuilt/packages/wget-{ver}-macos-64-clang.tar.7z"
            self.targetDigestUrls[ver] = f"https://files.kde.org/craft/prebuilt/packages/wget-{ver}-macos-64-clang.tar.7z.sha256"
            self.targetInstallPath[ver] = "dev-utils/wget"
        self.defaultTarget = "1.21.2-18"

    def setDependencies(self):
        self.buildDependencies["dev-utils/7zip"] = None
        self.buildDependencies["core/cacert"] = None


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def postInstall(self):
        return utils.createShim(self.imageDir() / "dev-utils/bin/wget", self.imageDir() / "dev-utils/wget/bin/wget",
         env = {"DYLD_LIBRARY_PATH": f"{CraftCore.standardDirs.craftRoot() / 'dev-utils/wget/lib'}"})

    def postQmerge(self):
        CraftCore.cache.clear()
        return True
