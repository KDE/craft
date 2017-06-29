# -*- coding: utf-8 -*-
import os

import info
from Package.CMakePackageBase import *

from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets["master"] = "https://github.com/KDAB/KDSoap.git"
        for ver in ["1.6.0"]:
            self.targets[ver] = f"https://github.com/KDAB/KDSoap/archive/kdsoap-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"KDSoap-kdsoap-{ver}"
            self.archiveNames[ver] = f"kdsoap-{ver}.tar.gz"
        self.targetDigests["1.6.0"] = (["3bedfdb5355096be434ed7cd7ce2529df823edbc75b6ca1ba4a48f0d647fd67e"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "1.6.0"
        self.shortDescription = "A Qt-based client-side and server-side SOAP component "


    def setDependencies( self ):
        self.dependencies["libs/qtbase"] = "default"


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
