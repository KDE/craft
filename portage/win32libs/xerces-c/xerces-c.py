import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['3.1.1']:
            self.targets[ver] = 'http://www.apache.org/dist/xerces/c/3/sources/xerces-c-' + ver + '.tar.gz'
            self.targetInstSrc[ver] = 'xerces-c-' + ver
        self.targetDigests['3.1.1'] = '177ec838c5119df57ec77eddec9a29f7e754c8b2'

        self.description = "A Validating XML Parser"
        self.defaultTarget = '3.1.1'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        if craftCompiler.isMSVC():
            self.buildDependencies["binary/xerces-c-bin"] = "default"


from Package.AutoToolsPackageBase import *
from Package.VirtualPackageBase import *


class PackageMSys(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)


if craftCompiler.isMinGW():
    class Package(PackageMSys):
        pass
else:
    class Package(VirtualPackageBase):
        pass
