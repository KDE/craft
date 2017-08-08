import info

from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['1.2.24'] = 'http://oligarchy.co.uk/xapian/1.2.24/xapian-core-1.2.24.tar.xz'
        self.targetDigests['1.2.24'] = '5c63be033157e030f41e128956b873fbd9ad6a1c'
        self.targetInstSrc['1.2.24'] = 'xapian-core-1.2.24'
        self.description = "Open Source Search Engine library"
        self.patchToApply['1.2.24'] = [("xapian-core-1.2.24-20170626.diff", 1)]
        self.defaultTarget = '1.2.24'

    def setDependencies(self):
        self.runtimeDependencies["win32libs/libxslt"] = "default"
        self.runtimeDependencies["virtual/base"] = "default"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
