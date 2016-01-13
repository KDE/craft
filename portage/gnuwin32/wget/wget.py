import info



class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets[ "1.17.1" ] = "http://downloads.sourceforge.net/sourceforge/tumagcc/wget-1.17.1_curl-7.46.0_win32_win64.7z"
        self.targetInstallPath[ "1.17.1" ] = "bin"
        self.targetDigests['1.17.1'] = (['0974c4576f24d38289b9958cc7fc41a64ef49e916ac7d4c148d741cd4981dac6'], EmergeHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.17.1"

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.merge.destinationPath = "dev-utils"

    def install( self ):
        if compiler.isX64():
            utils.copyFile(os.path.join(self.sourceDir(), "wget64.exe"), os.path.join(self.installDir(), "wget.exe"))
        else:
            utils.copyFile(os.path.join(self.sourceDir(), "wget.exe"), os.path.join(self.installDir(), "wget.exe"))
        utils.copyFile(os.path.join(self.sourceDir(), "curl-ca-bundle.crt"), os.path.join(self.installDir(), "curl-ca-bundle.crt"))
        return True