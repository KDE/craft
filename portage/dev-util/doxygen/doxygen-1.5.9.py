import base
import info

from Source.MultiSource import *
from BuildSystem.BinaryBuildSystem import *
from Package.PackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['1.5.9'] = 'http://ftp.stack.nl/pub/users/dimitri/doxygen-1.5.9.windows.bin.zip'
        self.defaultTarget = '1.5.9'
        # the zip file does not have a bin dir, so we have to create it  
        # This attribute is in prelimary state
        self.targetInstallPath['1.5.9'] = "bin";
        # merge the package into the dev-utils tree 
        # This attribute is in prelimary state
        self.targetMergePath['1.5.9'] = "dev-utils";
    
class Package(PackageBase, MultiSource, BinaryBuildSystem):
    def __init__( self):
        self.subinfo = subinfo()
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        BinaryBuildSystem.__init__(self)
        # no packager required 

if __name__ == '__main__':
    Package().execute()
