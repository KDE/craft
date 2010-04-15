import utils
import shutil
import os
import info

#  experimental wince compiler package  
#  todo: 
# - compiler requires -L %KDEROOT%/cegcc-arm-wince/arm-mingw32ce/lib 
#      with forward slashes for linking  (missing crt3.o) 
# - no working cmake generator available yet: 
#    'MinGW Makefiles' could not be used because compiler has problems 
#      with '\' path delimiter. 
#    'MSYS Makefiles' does not work too because cmd run from mingw32-make 
#      has problems with '/' path delimiters. 
#    'Unix Makefiles' generator does not work because cmd has problems 
#      with '/' path delimiters too
# - generated executable works on a wince 5.0 device 
#     tested with Microsoft Device Emulator 3.0 -- Standalone Release
#     http://www.microsoft.com/downloads/details.aspx?familyid=A6F6ADAF-12E3-4B2F-A394-356E2C2FB114

SRC_URI = """
http://downloads.sourceforge.net/project/cegcc/cegcc/0.59.1/cegcc_mingw32ce_cygwin1.7_r1399.tar.bz2
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.59.1'] = SRC_URI
        self.targetMergePath['0.59.1'] = "cegcc-arm-wince"
        # fixme: archive contains subdirs opt/mingw32ce, which is 
        # also created in the image dir
        self.targetMergeSourcePath['0.59.1'] = "opt\\mingw32ce"
        self.defaultTarget = '0.59.1'
            
from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        BinaryPackageBase.__init__(self)
    
    def unpack( self ):
        if not BinaryPackageBase.unpack(self):
            return False

        files = ['cygz.dll','cygwin1.dll','cyggcc_s-1.dll','cyggmp-3.dll','cygmpfr-1.dll']
        srcDir = self.packageDir()
        destDir = "%s/opt/mingw32ce/arm-mingw32ce/bin" % self.installDir()
        for file in files:
            utils.copyFile(os.path.join(srcDir,file),os.path.join(destDir,file));
        return True

if __name__ == '__main__':
    Package().execute()
