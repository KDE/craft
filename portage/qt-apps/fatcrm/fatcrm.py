# -*- coding: utf-8 -*-
import os

import info
from Package.CMakePackageBase import *

from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets["master"] = "https://github.com/KDAB/FatCRM.git|frameworks"
        self.defaultTarget = "master"

        self.shortDescription = "Desktop Application for SugarCRM"
        self.homepage = "http://www.kdab.com/"


    def setDependencies( self ):
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.dependencies["libs/qtbase"] = "default"
        self.dependencies["frameworks/kwallet"] = "default"
        self.dependencies["kde/akonadi"] = "default"
        self.dependencies["kde/kcontacts"] = "default"
        self.dependencies["kde/kcalcore"] = "default"
        self.dependencies["kde/akonadi-contacts"] = "default"
        self.dependencies["qt-libs/kdsoap"] = "default"
        self.dependencies["qt-libs/kdreports"] = "default"


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
