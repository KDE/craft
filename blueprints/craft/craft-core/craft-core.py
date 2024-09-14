import sys

import info
import utils
from CraftStandardDirs import CraftStandardDirs
from Package.BlueprintRepositoryPackageBase import BlueprintRepositoryPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["dev", "master", "qt5-lts"]:
            self.svnTargets[ver] = f"https://invent.kde.org/packaging/craft.git|{ver}|"
            self.targetUpdatedRepoUrl[ver] = (
                ["git://anongit.kde.org/craft", "https://invent.kde.org/kde/craft.git"],
                "https://invent.kde.org/packaging/craft.git",
            )
        self.defaultTarget = "master"

    def setDependencies(self):
        self.runtimeDependencies["virtual"] = None


class Package(BlueprintRepositoryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def checkoutDir(self, index=0):
        return CraftStandardDirs.craftRoot() / "craft"

    def unittest(self):
        test = self.sourceDir() / "bin/test/runtests.py"
        return utils.system([sys.executable, test])
