import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['3.8.1.0'] = 'http://sqlite.org/2013/sqlite-amalgamation-3080100.zip'
        self.targets['3.15.0'] = 'https://sqlite.org/2016/sqlite-amalgamation-3150000.zip'

        self.targetDigests['3.8.1.0'] = '75a1ab154e796d2d1b391a2c7078679e15512bda'
        self.targetDigests['3.15.0'] = (
            ['356109b55f76a9851f9bb90e8e3d722da222e26f657f76a471fdf4d7983964b9'], CraftHash.HashAlgorithm.SHA256)

        self.patchToApply['3.8.1.0'] = [("sqlite_cmake_and_wince_20130124.diff", 1)]
        self.patchToApply['3.15.0'] = [("sqlite-amalgamation-3150000-20161021.diff", 1)]

        self.targetInstSrc['3.8.1.0'] = "sqlite-amalgamation-3080100"
        self.targetInstSrc['3.15.0'] = "sqlite-amalgamation-3150000"

        self.description = "a library providing a self-contained, serverless, zero-configuration, transactional SQL database engine"
        self.defaultTarget = '3.15.0'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
