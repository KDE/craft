import base
import info
import os
import shutil
import utils

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.5.9'] = "http://downloads.sourceforge.net/sourceforge/gnuwin32/patch-2.5.9-7-bin.zip"
        self.defaultTarget = '2.5.9'
        self.targetMergePath['2.5.9'] = "dev-utils";

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'


from Source.ArchiveSource import *
from BuildSystem.BinaryBuildSystem import *
from Package.PackageBase import *

class Package(PackageBase, ArchiveSource, BinaryBuildSystem):
    def __init__( self):
        self.subinfo = subinfo()
        PackageBase.__init__(self)
        ArchiveSource.__init__(self)
        BinaryBuildSystem.__init__(self)
        # no packager required 

    def install( self ):
        BinaryBuildSystem.install( self )
        if self.compiler() == "msvc2005" or self.compiler() == "msvc2008":
            manifest = os.path.join( self.packageDir(), "patch.exe.manifest" )
            patch = os.path.join( self.installDir(), "bin", "patch.exe" )
            cmd = "mt.exe -nologo -manifest %s -outputresource:%s;1" % ( manifest, patch )
            utils.system( cmd )
    
        return True
        
if __name__ == '__main__':
    Package().execute()
