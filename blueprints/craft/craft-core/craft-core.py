import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2018.12", "master"]:
            self.svnTargets[ver] = f"git://anongit.kde.org/craft|{ver}|"
            self.targetUpdatedRepoUrl[ver] = ("git://anongit.kde.org/craft", "https://invent.kde.org/kde/craft.git")
        self.defaultTarget = "master"

    def setDependencies(self):
        self.runtimeDependencies["virtual"] = None

from Package.BlueprintRepositoryPackageBase import *


class Package(BlueprintRepositoryPackageBase):
    def __init__(self):
        BlueprintRepositoryPackageBase.__init__(self)

    def checkoutDir(self, index=0):
        return os.path.join(CraftStandardDirs.craftRoot(), "craft")

    def unittest(self):
        test = os.path.join(self.sourceDir(), "bin", "test", "runtests.py")
        return utils.system([sys.executable, test])
