import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["dev", "master"]:
            self.svnTargets[ver] = f"https://invent.kde.org/packaging/craft.git|{ver}|"
            self.targetUpdatedRepoUrl[ver] = (["git://anongit.kde.org/craft", "https://invent.kde.org/kde/craft.git"], "https://invent.kde.org/packaging/craft.git")
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
