import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2017.12", "master"]:
            self.svnTargets[ver] = f"git://anongit.kde.org/craft|{ver}|"
        self.defaultTarget = "master"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None

from Package.SourceOnlyPackageBase import *


class Package(SourceOnlyPackageBase):
    def __init__(self):
        SourceOnlyPackageBase.__init__(self)
        self.subinfo.options.package.disableBinaryCache = True
        self.subinfo.options.dailyUpdate = True

    def unpack(self):
        return True

    def install(self):
        return True

    def qmerge(self):
        if not SourceOnlyPackageBase.qmerge(self):
            return False
        CraftCore.cache.clear()
        return True

    def createPackage(self):
        return True

    def checkoutDir(self, index=0):
        return os.path.join(CraftStandardDirs.craftRoot(), "craft")

    def unittest(self):
        test = os.path.join(self.sourceDir(), "bin", "test", "runtests.py")
        return utils.system([sys.executable, test])
