import utils
from Package.PackageBase import *
from Package.VirtualPackageBase import *

class MaybeVirtualPackageBase(PackageBase):
    def __init__(self, condition, classA, classB=VirtualPackageBase):
        if condition or not craftSettings.getboolean("CraftDebug", "AllowToSkipPackages", True):
            package = classA
        else:
            package = classB
        MaybeVirtualPackageBase.__bases__ = (package,)
        MaybeVirtualPackageBase.__bases__[0].__init__(self)

