import utils
from Package.VirtualPackageBase import *

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
        newer = utils.utilsCache.checkVersionGreaterOrEqual(app=app, version=version, pattern=pattern, versionCommand=versionCommand)
        self.skipCondition  = not newer or not craftSettings.getboolean("CraftDebug", "AllowToSkipPackages", True)
        self.checkVersion = version
        MaybeVirtualPackageBase.__init__(self, condition=self.skipCondition, classA=classA, classB=classB)

        # override the install method
        def install():
            if not self.skipCondition:
                craftDebug.log.info(
                    f"Skipping installation of {self} as the installed version is >= {self.checkVersion}")
            return self.baseClass.install(self)

        setattr(self, "install", install)
