import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues("")

        self.homepage = 'http://www.boost.org/'

        self.shortDescription = 'portable C++ libraries'

    def setDependencies(self):
        self.runtimeDependencies["win32libs/boost/boost-headers"] = "default"
        self.runtimeDependencies["win32libs/boost/boost-bjam"] = "default"
        self.runtimeDependencies["win32libs/boost/boost-atomic"] = "default"
        self.runtimeDependencies["win32libs/boost/boost-graph"] = "default"
        self.runtimeDependencies["win32libs/boost/boost-program-options"] = "default"
        if self.options.features.pythonSupport:
            self.runtimeDependencies["win32libs/boost/boost-python"] = "default"
        self.runtimeDependencies["win32libs/boost/boost-regex"] = "default"
        self.runtimeDependencies["win32libs/boost/boost-system"] = "default"
        self.runtimeDependencies["win32libs/boost/boost-thread"] = "default"
        self.runtimeDependencies["win32libs/boost/boost-random"] = "default"
        self.runtimeDependencies["win32libs/boost/boost-iostreams"] = "default"
        self.runtimeDependencies["win32libs/boost/boost-filesystem"] = "default"
        self.runtimeDependencies["win32libs/boost/boost-date-time"] = "default"


from Package.VirtualPackageBase import *


class Package(VirtualPackageBase):
    def __init__(self):
        VirtualPackageBase.__init__(self)
