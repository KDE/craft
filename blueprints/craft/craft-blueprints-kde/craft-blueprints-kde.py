import os

import info
from CraftStandardDirs import CraftStandardDirs
from Package.BlueprintRepositoryPackageBase import BlueprintRepositoryPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["dev", "master", "qt5-lts"]:
            self.svnTargets[ver] = f"https://invent.kde.org/packaging/craft-blueprints-kde.git|{ver}|"
            self.targetUpdatedRepoUrl[ver] = (
                [
                    "git://anongit.kde.org/craft-blueprints-kde",
                    "https://invent.kde.org/kde/craft-blueprints-kde.git",
                ],
                "https://invent.kde.org/packaging/craft-blueprints-kde.git",
            )
        self.defaultTarget = "master"

    def setDependencies(self):
        self.buildDependencies["craft/craft-core"] = None


class Package(BlueprintRepositoryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def checkoutDir(self, index=0):
        # check for legacy dir
        checkoutDir = os.path.join(CraftStandardDirs.blueprintRoot(), "craft-kde")
        if not os.path.exists(checkoutDir):
            checkoutDir = super().checkoutDir()
        return checkoutDir
