import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.description = "python support for kdevelop"
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["extragear/kdevelop/kdevelop"] = "default"
        self.runtimeDependencies["extragear/kdevelop/kdev-php"] = "default"
        self.runtimeDependencies["binary/python-libs"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

        pythonExe = os.getenv('KDEV_PYTHON_PYTHON_EXECUTABLE', '')
        if pythonExe:
            self.subinfo.options.configure.args = f" -DPYTHON_EXECUTABLE=\"{pythonExe}\""
