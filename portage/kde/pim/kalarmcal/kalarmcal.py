# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.shortDescription = "KAlarm Akonadi Library"

    def setDependencies(self):
        self.buildDependencies['frameworks/extra-cmake-modules'] = 'default'
        self.runtimeDependencies['kde/akonadi'] = 'default'
        self.runtimeDependencies['kde/kcalcore'] = 'default'
        self.runtimeDependencies['kde/kidentitymanagement'] = 'default'
        self.runtimeDependencies['kde/kholidays'] = 'default'
        self.runtimeDependencies['frameworks/kdelibs4support'] = 'default'


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
