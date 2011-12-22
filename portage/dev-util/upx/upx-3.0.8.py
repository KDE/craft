import base
import info
import utils

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['3.0.8'] = "http://upx.sourceforge.net/download/upx308w.zip"
        self.targetDigests['3.0.8'] = 'a3c1494a667c71d267285d4a9ebc687a55f70485'
        self.defaultTarget = '3.0.8'

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
        shutil.copy(os.path.join( self.imageDir() , "upx308w", "upx.exe"),
                    os.path.join( self.installDir() , "bin" , "upx.exe") )
        utils.cleanDirectory( os.path.join( self.imageDir() , "upx308w" ) )
        os.removedirs( os.path.join( self.imageDir() , "upx308w" ) )
        return True

if __name__ == '__main__':
    Package().execute()
