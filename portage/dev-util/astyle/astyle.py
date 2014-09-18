import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.22'] = "http://www.winkde.org/pub/kde/ports/win32/repository/other/astyle-1.22-bin.zip"
        self.targets["2.0.4"] = "http://downloads.sourceforge.net/sourceforge/astyle/AStyle_2.04_windows.zip"
        self.targetMergeSourcePath["2.0.4"] = "AStyle"
        self.defaultTarget = '2.0.4'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.merge.destinationPath = "dev-utils"
        self.subinfo.options.merge.ignoreBuildType = True

