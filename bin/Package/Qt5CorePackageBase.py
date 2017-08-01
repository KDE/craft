#
# copyright (c) 2012 Hannah von Reth <vonreth@kde.org>
#
from BuildSystem.Qt5CoreBuildSystem import *
from Package.MaybeVirtualPackageBase import *
from Packager.TypePackager import *


class Qt5CorePackageBase(PackageBase, MultiSource, Qt5CoreBuildSystem, TypePackager):
    """provides a base class for qt5 modules"""

    def __init__(self):
        craftDebug.log.debug("Qt5CorePackageBase.__init__ called")
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        Qt5CoreBuildSystem.__init__(self)
        TypePackager.__init__(self)


class Qt5CoreSdkPackageBase(MaybeVirtualPackageBase):
    def __init__(self, condition=True, classA=Qt5CorePackageBase):
        sdkNotEnabled = not craftSettings.getboolean("QtSDK", "Enabled", False)
        MaybeVirtualPackageBase.__init__(self, condition and sdkNotEnabled, classA=classA)

        if not sdkNotEnabled:
            # override the install method
            def install():
                craftDebug.log.info(f"Skip installation of {self} as [QtSdk]Enabled=True")
                return self.baseClass.install(self)

            setattr(self, "install", install)
