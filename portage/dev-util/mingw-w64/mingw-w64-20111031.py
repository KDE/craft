import utils
import shutil
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in [ "20111031", "20111101" ]:
            self.targets[ver] = "http://downloads.sourceforge.net/sourceforge/mingw-w64/mingw-w64-bin_x86_64-mingw_"+ver+"_sezero.zip"
            
        ver = "4.8.2"
        rev = "3"
        self.targets[ "%s-%s" % ( ver, rev ) ] = "http://downloads.sourceforge.net/sourceforge/mingw-w64/x86_64-%s-release-posix-seh-rt_v3-rev%s.7z" % (ver, rev)
        self.targetDigests['4.8.2-3'] = 'f36476804806fe0b87e56fe94e5b93de5314b6f0'

        if self.options.features.legacyGCC:
            self.defaultTarget = "20111031"
        else:
            self.defaultTarget = "%s-%s" % ( ver, rev )

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
