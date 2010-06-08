import os
import info
import utils

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.5.9'] = "http://downloads.sourceforge.net/sourceforge/gnuwin32/patch-2.5.9-7-bin.zip"
        self.targetDigests['2.5.9'] = '7b2ec738881f4e962e54e0f330b67c42635266b7'
        self.defaultTarget = '2.5.9'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True
    
from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        BinaryPackageBase.__init__(self)

    def install( self ):
        if not BinaryPackageBase.install( self ): 
            return False
        if self.compiler() == "msvc2005" or self.compiler() == "msvc2008":
            manifest = os.path.join( self.packageDir(), "patch.exe.manifest" )
            patch = os.path.join( self.installDir(), "bin", "patch.exe" )
            cmd = "mt.exe -nologo -manifest %s -outputresource:%s;1" % ( manifest, patch )
            utils.system( cmd )
    
        return True
        
if __name__ == '__main__':
    Package().execute()
