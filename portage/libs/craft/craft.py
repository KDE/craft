import info
from Package import VirtualPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "[git]kde:craft"
        for ver in ["2017.05"]:
            self.svnTargets[ver] = f"[git]kde:craft|{ver}|"
        self.defaultTarget = "master"

    def setDependencies(self):
        self.buildDependencies['dev-util/git'] = 'default'
        self.buildDependencies['dev-util/7zip'] = 'default'


from Package.SourceOnlyPackageBase import *


class Package(SourceOnlyPackageBase):
    def __init__(self):
        SourceOnlyPackageBase.__init__(self)
        self.subinfo.options.package.disableBinaryCache = True

    def unpack(self):
        return True

    def fetch(self):
        return MultiSource.fetch(self)

    def install(self):
        return True

    def qmerge(self):
        utils.utilsCache.clear()
        return True

    def createPackage(self):
        return True

    def checkoutDir(self, index=0):
        return os.path.abspath(os.path.join(CraftStandardDirs.craftBin(), ".."))
