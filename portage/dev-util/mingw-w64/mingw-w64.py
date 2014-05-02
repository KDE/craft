import shutil
import os

import utils
import info


class subinfo(info.infoclass):
    def setTargets( self ):
        ver = "4.9.0"
        rev = "1"
        if compiler.isX64():
            self.targets[ "%s-%s" % ( ver, rev ) ] = "http://downloads.sourceforge.net/sourceforge/mingw-w64/x86_64-%s-release-posix-seh-rt_v3-rev%s.7z" % ( ver, rev )
            self.targetDigests['4.9.0-1'] = '208de028321e1ca4f4d3667a8d59e77be779a4c1'
        else:
            self.targets[ "%s-%s" % ( ver, rev )] = "http://downloads.sourceforge.net/sourceforge/mingw-w64/i686-%s-release-posix-sjlj-rt_v3-rev%s.7z" % ( ver, rev )
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
            if self.subinfo.buildTarget == "20111031":
                shutil.copy( os.path.join( self.installDir() , "mingw" , "bin" , "gmake.exe") , os.path.join( self.installDir() , "mingw" , "bin" , "mingw32-make.exe") )
                utils.applyPatch( self.imageDir(), os.path.join( self.packageDir(), "gcc_Exit.diff"), 0 )
        return True


