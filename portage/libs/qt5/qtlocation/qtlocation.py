# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "The Qt Location API helps you create viable mapping solutions" \
                                " using the data available from some of the popular location services."
        self.tags = "Qt5Positioning, Qt5Location"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"


from Package.Qt5CorePackageBase import *


class QtPackage(Qt5CorePackageBase):
    def __init__(self, **args):
        Qt5CorePackageBase.__init__(self)


class Package(Qt5CoreSdkPackageBase):
    def __init__(self):
        Qt5CoreSdkPackageBase.__init__(self, classA=QtPackage)
