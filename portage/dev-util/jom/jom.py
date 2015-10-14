# -*- coding: utf-8 -*-

import os

import info


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'

    def setTargets( self ):
        for ver in ['1_0_14','1_0_15','1_0_16']:
            self.targets[ver] = 'http://download.qt.io/official_releases/jom/jom_' + ver + '.zip'
        self.targetDigests['1_0_14'] = '5ae36ead8f0a877578b961acea80705416d23374'
        self.targetDigests['1_0_16'] = 'c4149fe706b25738b4c4e54c73e180b9cab55832'
        self.defaultTarget = '1_0_16'


from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = os.path.join("dev-utils","bin")

