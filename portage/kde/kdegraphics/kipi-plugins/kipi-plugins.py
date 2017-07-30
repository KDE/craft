# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "common KDE graphics application plugins"

    def setDependencies( self ):
        self.runtimeDependencies['frameworks/extra-cmake-modules'] = 'default'
        self.runtimeDependencies['frameworks/kconfig'] = 'default'
        self.runtimeDependencies['frameworks/kwindowsystem'] = 'default'
        self.runtimeDependencies['frameworks/kxmlgui'] = 'default'
        self.runtimeDependencies['frameworks/karchive'] = 'default'
        self.runtimeDependencies['frameworks/kio'] = 'default'
        self.runtimeDependencies['kde/libkipi'] = 'default'


class Package(CMakePackageBase):
    def __init__( self):
        CMakePackageBase.__init__(self)
