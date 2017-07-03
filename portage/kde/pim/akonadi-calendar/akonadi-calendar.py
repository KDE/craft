# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.shortDescription = "Akonadi Calendar library"

    def setDependencies( self ):
        self.buildDependencies['frameworks/extra-cmake-modules'] = 'default'
        self.runtimeDependencies['kde/akonadi'] = 'default'
        self.runtimeDependencies['kde/kcalcore'] = 'default'
        self.runtimeDependencies['kde/akonadi-contacts'] = 'default'
        self.runtimeDependencies['kde/kmailtransport'] = 'default'
        self.runtimeDependencies['kde/kcalutils'] = 'default'
        self.runtimeDependencies['kde/kidentitymanagement'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


