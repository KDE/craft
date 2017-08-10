import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "[git]kde:craft"
        for ver in ["2017.05", "gpg"]:
            self.svnTargets[ver] = f"[git]kde:craft|{ver}|"
        self.defaultTarget = "master"

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

    def fetch(self):
        git = utils.utilsCache.findApplication("git")
        if not utils.utilsCache.checkCommandOutputFor(git, "kde:",
                                                      "config --global --get url.git://anongit.kde.org/.insteadof"):
            craftDebug.log.debug("adding kde related settings to global git config file")
            utils.system(f"\"{git}\" config --global url.git://anongit.kde.org/.insteadOf kde:")
            utils.system(f"\"{git}\" config --global url.ssh://git@git.kde.org/.pushInsteadOf kde:")
            utils.system(f"\"{git}\" config --global core.autocrlf false")

        return SourceOnlyPackageBase.fetch(self)

    def install(self):
        return True

    def qmerge(self):
        if not SourceOnlyPackageBase.qmerge(self):
            return False
        utils.utilsCache.clear()
        return True

    def createPackage(self):
        return True

    def checkoutDir(self, index=0):
        return os.path.join(CraftStandardDirs.craftRoot(), "craft")
