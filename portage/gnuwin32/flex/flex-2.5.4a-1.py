# -*- coding: iso-8859-15 -*-
import base
import info
import os
import shutil
import utils

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.5.4a-1'] = "http://downloads.sourceforge.net/project/gnuwin32/flex/2.5.4a-1/flex-2.5.4a-1-bin.zip"
        self.targetDigests['2.5.4a-1'] = 'd68b456b2b52e7021eab993e5aa2826459b01cf2'
        self.defaultTarget = '2.5.4a-1'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True        
        self.subinfo.options.merge.destinationPath = "dev-utils";
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
