from Package.VirtualPackageBase import *
from Portage.CraftVersion import CraftVersion


class MaybeVirtualPackageBase(object):
    def __init__(self, condition, classA, classB=VirtualPackageBase):
        if condition:
            self.baseClass = classA
        else:
            self.baseClass = classB
        self.__class__.__bases__ = (self.baseClass,)
        self.__class__.__bases__[0].__init__(self)


class VirtualIfSufficientVersion(MaybeVirtualPackageBase):
    def __init__(self, app, version, classA, classB=VirtualPackageBase, pattern=None, versionCommand=None):
        appVersion = utils.utilsCache.getVersion(app, pattern, versionCommand)
        newer = appVersion and appVersion >= CraftVersion(version)
        self.skipCondition = not newer or not craftSettings.getboolean("CraftDebug", "AllowToSkipPackages", True)
        self.checkVersion = version
        MaybeVirtualPackageBase.__init__(self, condition=self.skipCondition, classA=classA, classB=classB)

        if not self.skipCondition:
            # override the install method
            def install():
                craftDebug.log.info(
                    f"Skipping installation of {self} as the installed version is >= {self.checkVersion}")
                return self.baseClass.install(self)

            def sourceRevision():
                return "system-installation: " + utils.utilsCache.findApplication(app)

            def version(self):
                return str(appVersion)

            setattr(self, "install", install)
            setattr(self, "sourceRevision", sourceRevision)
            setattr(self.__class__, "version", property(version))
