import info


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.MacOS

    def setTargets(self):
        self.svnTargets['master'] = "[git]https://github.com/packagesdev/packages.git"
        self.patchToApply["master"] = [("packagesdev-20191209.patch", 1)]
        for ver in ["1.2.6", "1.2.7"]:
           # self.patchToApply[ver] = [("packagesdev-20191209.patch", 1)]
            self.svnTargets[ver] = f"[git]https://github.com/packagesdev/packages.git||v{ver}"
        self.description = "Integrated Packaging Environment for OS X "
        self.webpage = "https://github.com/packagesdev/packages"
        self.defaultTarget = '1.2.7'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


from Package.MakeFilePackageBase import *


class Package(MakeFilePackageBase):
    def __init__(self):
        MakeFilePackageBase.__init__(self)
        self.subinfo.options.fetch.checkoutSubmodules = True
        self.subinfo.options.useShadowBuild = False

    def fetch(self):
        if isinstance(self, GitSource):
            if os.path.exists(self.sourceDir()):
                utils.system(["git", "clean", "-xdf"], cwd=self.sourceDir())
        return super().fetch()

    def make(self):
        return utils.system([Path(self.sourceDir()) / "build.sh" ])

    def install(self):
        dest = Path(self.imageDir()) / "bin"
        src = Path(self.sourceDir()) / "distribution/build"
        utils.createDir(dest)
        files = ["packagesbuild", "packagesutil"]
        for f in files:
            if not utils.copyFile(src / f, dest / f):
                return False
        return True