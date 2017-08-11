# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = "https://github.com/jrosdahl/ccache.git"
        self.targetInstallPath["master"] = "dev-utils"
        self.defaultTarget = 'master'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        if craftCompiler.isMinGW():
            self.buildDependencies["dev-util/msys"] = "default"


from Package.AutoToolsPackageBase import *
from Package.VirtualPackageBase import *


class PackageMinGW(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args = "--with-bundled-zlib "
        self.supportsCCACHE = False


if craftCompiler.isMinGW():
    class Package(PackageMinGW):
        def __init__(self):
            PackageMinGW.__init__(self)
else:
    class Package(VirtualPackageBase):
        def __init__(self):
            VirtualPackageBase.__init__(self)
