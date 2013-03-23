import utils
import shutil
import os
import info
import emergePlatform

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets["4.7.2"] = "http://downloads.sourceforge.net/sourceforge/mingwbuilds/%s-4.7.2-release-posix-sjlj-rev3.7z" % emergePlatform.buildArchitecture() 
        if emergePlatform.buildArchitecture() == 'x64':
            self.targets["4.8.0"] = "http://downloads.sourceforge.net/sourceforge/mingwbuilds/x64-4.8.0-release-posix-seh-rev0.7z"
            self.targetDigests['4.7.2'] = 'e4cc0963bbfe632fd4f7170767f5654ee6adb3c9'
        else:
            self.targets["4.8.0"] = "http://downloads.sourceforge.net/sourceforge/mingwbuilds/x32-4.8.0-release-posix-sjlj-rev0.7z"
        self.defaultTarget = "4.8.0"

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
