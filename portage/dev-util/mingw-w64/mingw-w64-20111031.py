import utils
import shutil
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in [ "20111031", "20111101" ]:
            self.targets[ver] = "http://downloads.sourceforge.net/sourceforge/mingw-w64/mingw-w64-bin_x86_64-mingw_"+ver+"_sezero.zip"
        
        self.targets["4.8.2-1"] = "http://downloads.sourceforge.net/sourceforge/mingw-w64/x86_64-4.8.2-release-posix-seh-rt_v3-rev1.7z"

        if self.options.features.legacyGCC:
            self.defaultTarget = "20111031"
        else:
            self.defaultTarget = "4.8.2-1"

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
