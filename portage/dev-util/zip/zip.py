import info
from Package.BinaryPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        repoUrl = """http://downloads.sourceforge.net/gnuwin32"""

        for version in ['2.31', '3.0']:
            self.targets[version] = [repoUrl + """/zip-""" + version + """-bin.zip""",
                                     repoUrl + """/zip-""" + version + """-dep.zip"""]
            self.targetInstallPath[version] = "dev-utils"

        self.targetDigests['3.0'] = ['58ae2b1f3e19811a1888f155c98297f763a4c5e7',
                                     '1326746e38470a04e58fa2146d3455b81265e0d8']
        self.defaultTarget = '3.0'

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = "default"


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
