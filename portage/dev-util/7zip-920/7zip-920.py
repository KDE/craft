import info
from CraftVersion import CraftVersion

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets["920"] = "http://www.7-zip.org/a/7za920.zip"
        self.targetInstallPath["920"] = os.path.join("dev-utils", "bin")
        self.targetDigests["920"] = (['2a3afe19c180f8373fa02ff00254d5394fec0349f5804e0ad2f6067854ff28ac'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "920"

from Package.BinaryPackageBase import *

class Package( BinaryPackageBase ):
    def __init__( self ):
        BinaryPackageBase.__init__( self )
        self.subinfo.options.packages.disableBinaryCache = True

    def install( self ):
        return utils.copyFile(os.path.join(self.sourceDir(), "7za.exe"), os.path.join(self.installDir(), "7za.exe"))
