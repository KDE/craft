import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["master", "2018.03"]:
            self.svnTargets[ver] = f"[git]git://anongit.kde.org/craft-blueprints-kde|{ver}|"
        self.defaultTarget = "master"

    def setDependencies(self):
        self.buildDependencies["dev-utils/git"] = "default"
        self.buildDependencies["dev-utils/7zip"] = "default"
        # make sure core is updated first
        self.buildDependencies["craft/craft-core"] = "default"


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
        # check for legacy dir
        checkoutDir = os.path.join(CraftStandardDirs.blueprintRoot(), "craft-kde")
        if not os.path.exists(checkoutDir):
            checkoutDir = os.path.join(CraftStandardDirs.blueprintRoot(), self.package.name)
        return checkoutDir
