import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2017.12"]:
            self.svnTargets[ver] = f"[git]git://anongit.kde.org/craft-blueprints-kde|{ver}|"
        self.defaultTarget = "2017.12"

    def setDependencies(self):
        self.buildDependencies["dev-util/git"] = "default"
        self.buildDependencies["dev-util/7zip"] = "default"


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
        return os.path.join(CraftStandardDirs.blueprintRoot(), "craft-kde")
