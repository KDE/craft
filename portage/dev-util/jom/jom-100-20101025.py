# -*- coding: utf-8 -*-
import base
import info
import shutil
import os

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

    def setTargets( self ):
        self.targets['HEAD'] = 'ftp://ftp.qt.nokia.com/jom/jom.zip'
        self.targets['094'] = 'ftp://ftp.qt.nokia.com/jom/jom094.zip'
        self.targetDigests['094'] = '1f946283866cd6f40a5888088f6c7d840b62af2d'
        self.targets['100'] = 'ftp://ftp.qt.nokia.com/jom/jom100.zip'
        self.targetDigests['100'] = '545e964c606d28edce582f167574298589970fb4'
        self.defaultTarget = '094'

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
