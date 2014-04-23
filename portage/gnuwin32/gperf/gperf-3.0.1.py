import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['3.0.1'] = "http://downloads.sourceforge.net/sourceforge/gnuwin32/gperf-3.0.1-bin.zip"
        self.targetDigests['3.0.1'] = 'ff74599cbdf8e970b7f3246da8b4b73909867c66'
        self.defaultTarget = '3.0.1'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils";
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
