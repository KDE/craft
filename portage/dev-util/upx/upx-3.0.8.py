
import info


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ( '3.0.8', '3.0.9' ):
            self.targets[ver] = 'http://upx.sourceforge.net/download/upx' + ver.replace('.', '') + 'w.zip'
        self.targetDigests['3.0.8'] = 'a3c1494a667c71d267285d4a9ebc687a55f70485'
        self.targetDigests['3.0.9'] = 'c735d341ecce5e44214f475db23222bf249a3eab'
        self.defaultTarget = '3.0.9'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        BinaryPackageBase.__init__(self)

    def install(self):
        ver2 = self.subinfo.buildTarget.replace('.', '')
        if not os.path.isdir( os.path.join( self.installDir() , "bin" ) ):
            os.makedirs( os.path.join( self.installDir() , "bin" ) )
        shutil.copy(os.path.join( self.imageDir() , "upx" + ver2 + "w", "upx.exe"),
                    os.path.join( self.installDir() , "bin" , "upx.exe") )
        utils.cleanDirectory( os.path.join( self.imageDir() , "upx" + ver2 + "w" ) )
        os.removedirs( os.path.join( self.imageDir() , "upx" + ver2 + "w" ) )
        return True

if __name__ == '__main__':
    Package().execute()
