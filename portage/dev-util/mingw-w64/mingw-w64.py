import shutil
import os

import utils
import info


class subinfo(info.infoclass):
    def setTargets( self ):
        ver = "5.3.0"
        rev = "0"
        if compiler.isX64():
            self.targets[ "%s-%s" % ( ver, rev ) ] = "http://downloads.sourceforge.net/sourceforge/mingw-w64/x86_64-%s-release-posix-seh-rt_v4-rev%s.7z" % ( ver, rev )
        else:
            self.targets[ "%s-%s" % ( ver, rev )] = "http://downloads.sourceforge.net/sourceforge/mingw-w64/i686-%s-release-posix-sjlj-rt_v4-rev%s.7z" % ( ver, rev )
            
        self.defaultTarget = "%s-%s" % ( ver, rev )

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.merge.ignoreBuildType = True

    def install(self):
        if not BinaryPackageBase.install(self):
            return False
        if compiler.isX86():
            return utils.moveDir( os.path.join( self.installDir() , "mingw32" ) , os.path.join( self.installDir(), "mingw" ) )
        return True


