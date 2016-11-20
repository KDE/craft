import info
import lzma

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in [ "1602"]:
            self.targets[ ver ] = "http://www.7-zip.org/a/7z%s-extra.7z" % ver
            self.targetInstallPath[ ver ] = "bin"
        self.targetDigests['1602'] = (['f6c412e8bc45e4a88e675976024c21ed7a23eeb7eb0af452aa7a9b9a97843aa2'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '1602'


    def setDependencies( self ):
        self.buildDependencies[ 'gnuwin32/wget' ] = 'default'

from Package.BinaryPackageBase import *

class Package( BinaryPackageBase ):
    def __init__( self ):
        BinaryPackageBase.__init__( self )
        self.subinfo.options.merge.destinationPath = "dev-utils"

    def install( self ):
        if compiler.isX64():
            return utils.copyFile(os.path.join(self.sourceDir(), "x64", "7za.exe"), os.path.join(self.installDir(), "7za.exe"))
        else:
            return utils.copyFile(os.path.join(self.sourceDir(), "7za.exe"), os.path.join(self.installDir(), "7za.exe"))
