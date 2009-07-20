import os
import shutil
import utils
import info

from Source.MultiSource import *
from BuildSystem.CMakeBuildSystem import *
from Packager.MultiPackager import *
from Package.PackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.15.1b'] = 'ftp://ftp.mars.org/pub/mpeg/libmad-0.15.1b.tar.gz'
        self.targetInstSrc['0.15.1b'] = 'libmad-0.15.1b'
        self.defaultTarget = '0.15.1b'        
                
class Package(PackageBase, MultiSource, CMakeBuildSystem, MultiPackager):
    def __init__( self ):
        # we use subinfo for now too 
        self.subinfo = subinfo()
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        CMakeBuildSystem.__init__(self)        
        MultiPackager.__init__(self)

    def unpack( self ):
        MultiSource.unpack( self ) or utils.die( "unpack failed" )
        shutil.copyfile( os.path.join( self.packagedir, "CMakeLists.txt" ), os.path.join( self.sourceDir(), "CMakeLists.txt" ) )
        shutil.copyfile( os.path.join( self.packagedir, "FindKDEWIN.cmake" ), os.path.join( self.sourceDir(), "FindKDEWIN.cmake" ) )
        return True

if __name__ == '__main__':
    Package().execute()

