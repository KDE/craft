import shutil
import os

import utils
import info


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver, rev, rt in [("5.3.0", "0", "4"), ("5.4.0", "0", "5"),("6.2.0", "0", "5")]:
            if compiler.isX64():
                self.targets[ "%s-%s" % ( ver, rev ) ] = "http://downloads.sourceforge.net/sourceforge/mingw-w64/x86_64-%s-release-posix-seh-rt_v%s-rev%s.7z" % ( ver, rt, rev )
            else:
                self.targets[ "%s-%s" % ( ver, rev )] = "http://downloads.sourceforge.net/sourceforge/mingw-w64/i686-%s-release-posix-sjlj-rt_v%s-rev%s.7z" % ( ver, rt, rev )
            
        self.defaultTarget = "5.4.0-0"

    def setDependencies( self ):
        self.dependencies['virtual/bin-base'] = 'default'

from Package.BinaryPackageBase import *

class PackageMinGW(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)

    def install(self):
        if not BinaryPackageBase.install(self):
            return False
        if compiler.isX86():
            return utils.moveDir( os.path.join( self.installDir() , "mingw32" ) , os.path.join( self.installDir(), "mingw" ) )
        return True



from Package.Qt5CorePackageBase import *

class Package( Qt5CoreSdkPackageBase ):
    def __init__(self):
        Qt5CoreSdkPackageBase.__init__(self, condition=compiler.isMinGW(), classA=PackageMinGW)