# -*- coding: utf-8 -*-

import info
import shutil
import os

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'

    def setTargets( self ):
        self.targets['HEAD'] = 'ftp://ftp.qt.nokia.com/jom/jom.zip'
        for ver in ['0_9_04', '1_0_00', '1_0_01', '1_0_02', '1_0_03', '1_0_04',
                    '1_0_05', '1_0_06', '1_0_07', '1_0_08', '1_0_09', '1_0_10',
                    '1_0_11', '1_0_12', '1_0_13']:
            self.targets[ver] = 'http://releases.qt-project.org/jom/jom_' + ver + '.zip'
        self.targets['unstable'] = 'ftp://ftp.qt.nokia.com/jom/unstable-jom.zip'
        self.targetDigests['0_9_04'] = '1f946283866cd6f40a5888088f6c7d840b62af2d'
        self.targetDigests['1_0_00'] = '545e964c606d28edce582f167574298589970fb4'
        self.targetDigests['1_0_01'] = '3cbc2750a8a0b8c736a10c7445b0b92ecf247292'
        self.targetDigests['1_0_02'] = '9cda65f2de954a3236d79f6bc72f5561da32163f'
        self.targetDigests['1_0_03'] = 'bb4c0a1db803a3ed8c31da29b1ad672bbcc636cb'
        self.targetDigests['1_0_05'] = '47c0b3fb58a753bb32b707528adc10bebf2b028a'
        self.targetDigests['1_0_08'] = '5efb1ada73d2886722ce0473b1b79de0bef38e1d'
        self.targetDigests['1_0_09'] = '6d58c5353dca65ca9ec4843ef394876ab4db179d'
        self.targetDigests['1_0_11'] = '089a6cc6a0366d480731be2d5cb608f7a54b8104'
        self.targetDigests['1_0_12'] = '751acb5f71c022948553e006edd1aff2662c0b03'
	self.targetDigests['1_0_13'] = 'e4059a58be58d04e70a1935b6886e28b69be7b82'
        self.targets['1_0_1-patched'] = 'http://www.winkde.org/pub/kde/ports/win32/repository/other/jom101-patched.7z'
        self.targetDigests['1_0_1-patched'] = '5f878e50cdd05f390b2737d4050a740edd48337f'
        self.targetDigests['unstable'] = '04feebc828bd30b3490890f04dc6b8ed7949e070'
        self.defaultTarget = '1_0_13'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = os.path.join("dev-utils","bin")
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
