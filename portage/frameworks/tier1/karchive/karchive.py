import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Qt 5 addon providing access to numerous types of archives"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/qt5/qttools"] = "default"
        self.runtimeDependencies["win32libs/libbzip2"] = "default"
        self.runtimeDependencies["win32libs/zlib"] = "default"
        if not craftCompiler.isMSVC2010() and not craftCompiler.isMSVC2012():
            self.runtimeDependencies["win32libs/liblzma"] = "default"

        for ver in ('5.0.0', '5.1.0', '5.2.0'):
            self.patchToApply[ver] = [('get-rid-of-VLAs.diff', 1)]


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
