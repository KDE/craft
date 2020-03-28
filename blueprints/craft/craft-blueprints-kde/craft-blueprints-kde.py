import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2018.12", "2019.04", "master"]:
            self.svnTargets[ver] = f"[git]https://anongit.kde.org/craft-blueprints-kde|{ver}|"
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
