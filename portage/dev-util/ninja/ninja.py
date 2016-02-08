# -*- coding: utf-8 -*-

import os

import info


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'

    def setTargets( self ):
        for ver in ["1.6.0" ]:
            self.targets[ ver ] = "https://github.com/ninja-build/ninja/releases/download/v%s/ninja-win.zip" % ver
            self.targetInstallPath[ ver ] = "bin"
            self.archiveNames[ ver] = "ninja-win%s.zip" % ver

        self.targetDigests['1.6.0'] = (['18f55bc5de27c20092e86ace8ef3dd3311662dc6193157e3b65c6bc94ce006d5'], EmergeHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.6.0"



from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.merge.destinationPath = "dev-utils"

