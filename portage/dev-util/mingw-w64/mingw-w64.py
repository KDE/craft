import shutil
import os

import utils
import info


class subinfo(info.infoclass):
    def setTargets( self ):
        ver = "4.9.2"
        rev = "0"
        if compiler.isX64():
            self.targets[ "%s-%s" % ( ver, rev ) ] = "http://downloads.sourceforge.net/sourceforge/mingw-w64/x86_64-%s-release-posix-seh-rt_v3-rev%s.7z" % ( ver, rev )
            self.targetDigests['4.9.1-0'] = 'd826187ad09ae53ae9596f8d69dd44fd944af36a'
        else:
            self.targets[ "%s-%s" % ( ver, rev )] = "http://downloads.sourceforge.net/sourceforge/mingw-w64/i686-%s-release-posix-sjlj-rt_v3-rev%s.7z" % ( ver, rev )
            self.targetDigests['4.9.1-0'] = 'c4560bef20eef59bb886feccb2e0eb51f8d27f8b'
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
            shutil.move( os.path.join( self.installDir() , "mingw32" ) , os.path.join( self.installDir(), "mingw" ) )
        return True


