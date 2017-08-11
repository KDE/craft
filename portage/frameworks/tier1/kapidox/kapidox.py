import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Scripts and data for building API documentation (dox) in a standard format and style."

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/cmake"] = "default"
        self.runtimeDependencies["dev-util/python3"] = "default"
        self.runtimeDependencies["dev-util/doxygen"] = "default"
        self.runtimeDependencies["python-modules/pyyaml"] = "default"
        self.runtimeDependencies["python-modules/jinja2"] = "default"
        self.runtimeDependencies["python-modules/doxyqml"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        # the shims are not portable
        self.subinfo.options.package.disableBinaryCache = True

    def install(self):
        if not CMakeBuildSystem.install(self):
            return False
        binPath = os.path.join(self.imageDir(), "bin")
        for script in ["depdiagram-generate", "depdiagram-generate-all", "depdiagram-prepare", "kapidox_generate"]:
            if not utils.createShim(os.path.join(binPath, f"{script}.exe"),
                                    os.path.join(self.imageDir(), "dev-utils", "bin", "python2.exe"),
                                    args=os.path.join(CraftStandardDirs.craftRoot(), "Scripts", script)):
                return False
        return True
