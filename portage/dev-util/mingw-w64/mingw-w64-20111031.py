import utils
import shutil
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in [ "20111031", "20111101" ]:
            self.targets[ver] = "http://downloads.sourceforge.net/sourceforge/mingw-w64/mingw-w64-bin_x86_64-mingw_"+ver+"_sezero.zip"
        
        self.targets["4.7.2"] = "http://downloads.sourceforge.net/sourceforge/mingwbuilds/%s-4.7.2-release-posix-sjlj-rev3.7z" % emergePlatform.buildArchitecture()
        self.targetDigests['4.7.2'] = 'e4cc0963bbfe632fd4f7170767f5654ee6adb3c9'
        self.targets["4.8.1-2"] = "http://downloads.sourceforge.net/sourceforge/mingwbuilds/%s-4.8.1-release-posix-seh-rev2.7z" % emergePlatform.buildArchitecture()

        self.defaultTarget = "20111031"

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
