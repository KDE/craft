# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.shortDescription = "Akonadi Calendar library"

    def setDependencies( self ):
        self.buildDependencies['frameworks/extra-cmake-modules'] = 'default'
        self.dependencies['kde/akonadi'] = 'default'
        self.dependencies['kde/kcalcore'] = 'default'
        self.dependencies['kde/akonadi-contacts'] = 'default'
        self.dependencies['kde/kmailtransport'] = 'default'
        self.dependencies['kde/kcalutils'] = 'default'
        self.dependencies['kde/kidentitymanagement'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


