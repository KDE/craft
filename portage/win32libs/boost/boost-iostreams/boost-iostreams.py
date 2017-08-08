import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues("", tarballInstallSrc=self.package.package.name.replace("boost-", "").replace("-", "_"))

        self.webpage = 'http://www.boost.org/'

        self.description = 'portable C++ libraries'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["win32libs/boost/boost-headers"] = "default"
        self.buildDependencies["win32libs/boost/boost-bjam"] = "default"
        self.runtimeDependencies["win32libs/zlib"] = "default"


from Package.BoostPackageBase import *


class Package(BoostPackageBase):
    def __init__(self, **args):
        BoostPackageBase.__init__(self)
        self.subinfo.options.configure.args = "-s NO_BZIP2=1"
