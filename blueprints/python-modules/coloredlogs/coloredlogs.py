import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["15.0.1"]:
            self.svnTargets[ver] = ""
        self.defaultTarget = "15.0.1"
        self.releaseManagerId = 74372
        self.webpage = "https://pypi.org/project/coloredlogs/"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/pip"] = None
        self.buildDependencies["python-modules/setuptools"] = None
        self.runtimeDependencies["libs/python"] = None
        self.runtimeDependencies["python-modules/humanfriendly"] = None
        self.buildDependencies["dev-utils/system-python3"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
