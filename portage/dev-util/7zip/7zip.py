import info
import lzma

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in [ "1512", "1514"]:
            self.targets[ ver ] = "http://downloads.sourceforge.net/sourceforge/sevenzip/7z%s-extra.7z" % ver
            self.targetInstallPath[ ver ] = "bin"
        self.targetDigests['1512'] = '0772dcf51fd7d22ac8ac04976e8c2a2f8cbe5ccd'
        self.targetDigests['1514'] = (['4fb7b51e93cabbede23281eae0d024a63f485dc339c85e20c305f328a76e90c0'], EmergeHash.HashAlgorithm.SHA256)
        self.defaultTarget = '1514'


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
