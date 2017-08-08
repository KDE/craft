import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Runtime and library to organize the user work in separate activities"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["frameworks/tier3/kservice"] = "default"
        self.runtimeDependencies["frameworks/tier3/kio"] = "default"
        self.runtimeDependencies["win32libs/boost/boost-headers"] = "default"

        # those are only needed for building the activity manager daemon


# self.runtimeDependencies['win32libs/boost-range'] = 'default'
#        self.runtimeDependencies['win32libs/boost-containers'] = 'default'

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DKACTIVITIES_LIBRARY_ONLY=YES"
