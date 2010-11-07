import base
import info
import utils

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['3.0.7'] = "http://upx.sourceforge.net/download/upx307w.zip"
        self.targetDigests['3.0.7'] = 'fbc3ea009cf90d32a49a619aa7fc46aab0f1a4e4'
        self.defaultTarget = '3.0.7'
    
from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        BinaryPackageBase.__init__(self)
        
    def install(self):
        if not os.path.isdir( os.path.join( self.installDir() , "bin" ) ):
            os.makedirs( os.path.join( self.installDir() , "bin" ) )
        shutil.copy(os.path.join( self.imageDir() , "upx307w", "upx.exe"),
                    os.path.join( self.installDir() , "bin" , "upx.exe") )
        utils.cleanDirectory( os.path.join( self.imageDir() , "upx307w" ) )
        os.removedirs( os.path.join( self.imageDir() , "upx307w" ) )
        return True

if __name__ == '__main__':
    Package().execute()
