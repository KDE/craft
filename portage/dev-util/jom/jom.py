# -*- coding: utf-8 -*-

import os

import info


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'

    def setTargets( self ):
        for ver in ['1_0_14','1_0_15','1_0_16']:
            self.targets[ver] = 'http://download.qt.io/official_releases/jom/jom_' + ver + '.zip'
            self.targetDigestUrls[ver] = (["http://download.qt.io/official_releases/jom/md5sums.txt"], EmergeHash.HashAlgorithm.MD5)
        self.defaultTarget = '1_0_16'


from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = os.path.join("dev-utils","bin")

