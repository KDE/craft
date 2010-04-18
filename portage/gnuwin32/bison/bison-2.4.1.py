# -*- coding: iso-8859-15 -*-
import base
import info
import os
import shutil
import utils

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.4.1'] = """http://downloads.sourceforge.net/project/gnuwin32/bison/2.4.1/bison-2.4.1-bin.zip
                                 http://downloads.sourceforge.net/project/gnuwin32/bison/2.4.1/bison-2.4.1-dep.zip"""
        self.targetDigests['2.4.1'] = ['2e05049a8519ea6b802553adf7b46da358e05c81',
                                       '820e44f4d0d87c3fdff00cb823388b9cc9e1941b']                                 
        self.defaultTarget = '2.4.1'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True        
        self.subinfo.options.merge.destinationPath = "dev-utils";
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
