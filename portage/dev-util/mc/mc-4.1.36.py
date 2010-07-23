import base
import os
import shutil
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['4.1.36'] = "http://www.siegward-jaekel.de/mc.zip"
        self.defaultTarget = '4.1.36'
        self.targetInstallPath['4.1.36'] = "bin"
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        
from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        BinaryPackageBase.__init__(self)

    def install( self ):
        f = open(os.path.join(self.installDir(), 'mcedit.bat'), "wb")
        f.write("mc -e %1")
        f.close()
        # mc is also a program in visual studio,
        # so make the real mc reachable from mcc too...
        utils.copyFile(os.path.join(self.installDir(), "mc.exe"), 
            os.path.join( self.installDir(), "mcc.exe"))
        return True

if __name__ == '__main__':
    Package().execute()
