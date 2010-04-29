import utils
import shutil
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['20100428'] = "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/sezero_20100428_new/mingw-w64-bin_x86_64-mingw_20100428_sezero.zip"
        self.defaultTarget = '20100428'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        self.hardDependencies['gnuwin32/patch'] = 'default'
        
from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        BinaryPackageBase.__init__(self)
		
    def install(self):
        if not BinaryPackageBase.install():
          return False
        shutil.copy(os.path.join( self.installDir() , "mingw64" , "bin" , "gmake.exe") , os.path.join( self.installDir() , "mingw64" , "bin" , "mingw32-make.exe") )
        return True

if __name__ == '__main__':
    Package().execute()
