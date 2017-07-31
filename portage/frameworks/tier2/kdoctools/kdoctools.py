import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.shortDescription = "Documentation generation from docbook "

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/perl"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qtbase"] = "default"
        self.runtimeDependencies["frameworks/karchive"] = "default"
        self.runtimeDependencies["frameworks/ki18n"] = "default"
        self.runtimeDependencies["win32libs/libxslt"] = "default"
        self.runtimeDependencies["data/docbook-dtd"] = "default"
        self.runtimeDependencies["data/docbook-xsl"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        # this package is currently not portable due to hardcoded path in the xml files
        self.subinfo.options.package.disableBinaryCache = True
