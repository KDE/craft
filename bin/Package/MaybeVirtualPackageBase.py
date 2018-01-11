from Package.VirtualPackageBase import *
from Blueprints.CraftVersion import CraftVersion
import Utils.CraftCache


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
        app = CraftCore.cache.findApplication(app)
        appVersion = not app.startswith(CraftCore.standardDirs.craftRoot()) and CraftCore.cache.getVersion(app, pattern, versionCommand)
        newer = appVersion and appVersion >= CraftVersion(version)
        self.skipCondition = not newer or not CraftCore.settings.getboolean("CraftDebug", "AllowToSkipPackages", True)
        self.checkVersion = version
        MaybeVirtualPackageBase.__init__(self, condition=self.skipCondition, classA=classA, classB=classB)

        if not self.skipCondition:
            # override the install method
            def install():
                CraftCore.log.info(
                    f"Skipping installation of {self} as the installed version of {app} {appVersion} >= {self.checkVersion}")
                return self.baseClass.install(self)

            def sourceRevision():
                return f"system-installation: {app}"

            def version(self):
                return str(appVersion)

            setattr(self, "install", install)
            setattr(self, "sourceRevision", sourceRevision)
            setattr(self.__class__, "version", property(version))
