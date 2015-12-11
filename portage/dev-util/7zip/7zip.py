import info
import lzma

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in [ "1512"]:
            self.targets[ ver ] = "http://downloads.sourceforge.net/sourceforge/sevenzip/7z%s-extra.7z" % ver
            self.targetInstallPath[ ver ] = "bin"
        self.targetDigests['1512'] = '0772dcf51fd7d22ac8ac04976e8c2a2f8cbe5ccd'
        self.defaultTarget = '1512'


    def setDependencies( self ):
        self.buildDependencies[ 'gnuwin32/wget' ]       = 'default'

from Package.BinaryPackageBase import *

class Package( BinaryPackageBase ):
    def __init__( self ):
        BinaryPackageBase.__init__( self )
        self.subinfo.options.merge.destinationPath = "dev-utils"

    def unpack(self):
        utils.cleanDirectory(self.imageDir())
        self.checkDigest()
        bin = os.path.join(self.imageDir(), "bin")
        os.makedirs(bin)
        path = "7za.exe"
        if compiler.isX64():
            path = "x64/7za.exe"
        return utils.system("%s/7za.exe e %s %s" %( self.packageDir(), os.path.join(EmergeStandardDirs.downloadDir(), self.localFileNames()[0]), path), cwd = bin)