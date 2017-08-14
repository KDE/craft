# -*- coding: utf-8 -*-

import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["svnHEAD"] = "http://source.icu-project.org/repos/icu/icu/trunk"
        self.targetInstSrc["svnHEAD"] = "source"
        for ver in ["53.1", "55.1", "58.2"]:
            ver2 = ver.replace(".", "_")
            self.targets[ver] = f"http://download.icu-project.org/files/icu4c/{ver}/icu4c-{ver2}-src.tgz"
            self.targetDigestUrls[ver] = (
                [f"https://ssl.icu-project.org/files/icu4c/{ver}/icu4c-src-{ver2}.md5"], CraftHash.HashAlgorithm.MD5)
            self.targetInstSrc[ver] = os.path.join("icu", "source")
        if craftCompiler.isMSVC2015() or craftCompiler.isMinGW():
            self.patchToApply["55.1"] = ("icu-20150414.diff", 2)
        if craftCompiler.isMinGW():
            self.patchToApply["55.1"] = [("icu-20150414.diff", 2), ("icu-msys.diff", 2)]
            self.patchToApply["58.2"] = ("0020-workaround-missing-locale.patch",
                                         2)  # https://raw.githubusercontent.com/Alexpux/MINGW-packages/master/mingw-w64-icu/0020-workaround-missing-locale.patch

        self.defaultTarget = "58.2"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        if craftCompiler.isMinGW():
            self.buildDependencies["dev-util/msys"] = "default"


from Package.MSBuildPackageBase import *


class PackageCMake(MSBuildPackageBase):
    def __init__(self, **args):
        MSBuildPackageBase.__init__(self)

        if craftCompiler.isX86():
            self.subinfo.options.configure.args = " /p:Platform=Win32"
        self.subinfo.options.configure.projectFile = os.path.join(self.sourceDir(), "allinone", "allinone.sln")

    def install(self):
        self.cleanImage()
        if not MSBuildPackageBase.install(self, installHeaders=False,
                                          buildDirs=[os.path.join(self.sourceDir(), "..", dir) for dir in
                                                     ["bin", "bin64", "lib", "lib64"]]):
            return False
        utils.copyDir(os.path.join(self.sourceDir(), "..", "include"), os.path.join(self.imageDir(), "include"))

        if craftCompiler.isMSVC() and self.buildType() == "Debug":
            imagedir = os.path.join(self.installDir(), "lib")
            filelist = os.listdir(imagedir)
            for f in filelist:
                if f.endswith("d.lib"):
                    utils.copyFile(os.path.join(imagedir, f), os.path.join(imagedir, f.replace("d.lib", ".lib")))

        return True


from Package.AutoToolsPackageBase import *


class PackageMSys(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)

    def make(self):
        datafile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icudt55l.dat")
        if os.path.exists(datafile):
            datafileDestination = os.path.join(self.sourceDir(), "data", "in", "icudt55l.dat")
            if os.path.exists(datafileDestination):
                os.remove(datafileDestination)
            utils.copyFile(datafile, datafileDestination)

        return AutoToolsPackageBase.make(self)

    def install(self):
        if not AutoToolsPackageBase.install(self):
            return False
        files = os.listdir(os.path.join(self.installDir(), "lib"))
        for dll in files:
            if dll.endswith(".dll"):
                utils.copyFile(os.path.join(self.installDir(), "lib", dll), os.path.join(self.installDir(), "bin", dll))
        return True


if craftCompiler.isMinGW():
    class Package(PackageMSys):
        pass
else:
    class Package(PackageCMake):
        pass
