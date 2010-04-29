import utils
import shutil
import os
import info

SRC_URI = """
http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/sezero_20100410/mingw-w64-bin_x86_64-mingw_20100410_sezero.zip
http://downloads.sourceforge.net/sourceforge/mingw/mingw32-make-3.81-20080326.tar.gz
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['20100411'] = SRC_URI
        self.targetMergePath['20100411'] = ""
        self.defaultTarget = '20100411'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        self.hardDependencies['gnuwin32/patch'] = 'default'
        
from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
