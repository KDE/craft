import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["dev", "master"]:
            self.svnTargets[ver] = f"https://invent.kde.org/packaging/craft-blueprints-kde.git|{ver}|"
            self.targetUpdatedRepoUrl[ver] = (["git://anongit.kde.org/craft-blueprints-kde", "https://invent.kde.org/kde/craft-blueprints-kde.git"], "https://invent.kde.org/packaging/craft-blueprints-kde.git")
        self.defaultTarget = "master"

    def setDependencies(self):
        self.buildDependencies["craft/craft-core"] = None


from Package.BlueprintRepositoryPackageBase import *


class Package(BlueprintRepositoryPackageBase):
    def __init__(self):
        BlueprintRepositoryPackageBase.__init__(self)

    def checkoutDir(self, index=0):
        # check for legacy dir
        checkoutDir = os.path.join(CraftStandardDirs.blueprintRoot(), "craft-kde")
        if not os.path.exists(checkoutDir):
            checkoutDir = super().checkoutDir()
        return checkoutDir
