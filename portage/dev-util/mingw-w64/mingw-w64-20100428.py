import utils
import shutil
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['20100427-old'] = "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/sezero_20100427_old/mingw-w64-bin_x86_64-mingw_20100427_sezero.zip"
        self.targetDigests['20100427-old'] = '0d1d8e67fe86bfd125e497dae18e55d691ad0f1a'
	self.patchToApply['20100427-old'] = ( "gcc_Exit.diff" , 1 )
        
        self.targets['20100513'] = "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/sezero_20100513/mingw-w64-bin_x86_64-mingw_20100513_sezero.zip"
        self.targetDigests['20100513'] = 'a1f17230808b2b8d6f806b86aaea52a869e391af'
        self.targets['20100527'] = "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/sezero_20100527/mingw-w64-bin_x86_64-mingw_20100527_sezero.zip"
        self.targetDigests['20100527'] = '53b65ce9d5602154177a88af54d065ad00ea7bc1'
        self.defaultTarget = '20100527'
            
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
        shutil.copy(os.path.join( self.installDir() , "mingw64" , "bin" , "gmake.exe") , os.path.join( self.installDir() , "mingw64" , "bin" , "mingw32-make.exe") )
        return True

if __name__ == '__main__':
    Package().execute()
