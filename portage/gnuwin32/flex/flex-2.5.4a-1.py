# -*- coding: iso-8859-15 -*-

import info
import os
import shutil
import utils

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.5.4a-1'] = """
http://downloads.sourceforge.net/project/gnuwin32/flex/2.5.4a-1/flex-2.5.4a-1-bin.zip
http://switch.dl.sourceforge.net/project/gnuwin32/flex/2.5.4a-1/flex-2.5.4a-1-lib.zip"""
        self.targetDigests['2.5.4a-1'] = ['d68b456b2b52e7021eab993e5aa2826459b01cf2','6b21fa545496f2832a5f1404ecba94291e4a4075']
        self.defaultTarget = '2.5.4a-1'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils";
        BinaryPackageBase.__init__(self)
        
    def install(self):
        if not BinaryPackageBase.install(self):
            return False
        utils.copyFile(os.path.join(self.imageDir(),"lib","libfl.a"),os.path.join(self.imageDir(),"lib","fl.lib"))#yes using a static mingw lib with msvc is very evil, but it seems works
        os.remove(os.path.join(self.imageDir(),"include","unistd.h"))#would corrup winkde includes
        return True

if __name__ == '__main__':
    Package().execute()
