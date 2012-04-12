# -*- coding: utf-8 -*-
import utils
import shutil
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        ver = "20111031"
        self.targets[ver] = "http://downloads.sourceforge.net/sourceforge/mingw-w64/mingw-w32-bin_i686-mingw_"+ver+"_sezero.zip"

        for ver in [ "4.6.4" ]:
            self.targets["4.6.4"] = "http://downloads.sourceforge.net/sourceforge/mingw-w64/i686-w64-mingw32-gcc-4.6.4_rubenvb.7z"
        self.targetDigests['4.6.4'] = 'f1117b60d089cfa0e18e5ec675eac6afc4e46136'
        self.defaultTarget = "4.6.4"

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        BinaryPackageBase.__init__(self)

    def install(self):
        shutil.move( os.path.join( self.installDir() , "mingw32" ) , os.path.join( self.installDir(), "mingw" ) )
        return True
if __name__ == '__main__':
    Package().execute()
