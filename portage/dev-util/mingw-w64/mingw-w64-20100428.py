import utils
import shutil
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):        
        ver = "20101003"
        self.targets[ver] = "http://downloads.sourceforge.net/sourceforge/mingw-w64/mingw-w64-bin_x86_64-mingw_"+ver+"_sezero.zip"
        self.defaultTarget = ver
            
    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'
        
from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        BinaryPackageBase.__init__(self)

    def install(self):
        utils.applyPatch( self.imageDir(), os.path.join( self.packageDir(), "gcc_Exit.diff"), 1 )
        shutil.copy(os.path.join( self.installDir() , "mingw64" , "bin" , "gmake.exe") , os.path.join( self.installDir() , "mingw64" , "bin" , "mingw32-make.exe") )
        return True

if __name__ == '__main__':
    Package().execute()
