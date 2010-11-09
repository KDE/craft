import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.9.6'] = "http://www.winkde.org/pub/kde/ports/win32/installer/kdewin-packager.exe"
        self.defaultTarget = '0.9.6'
        ## \todo specific a target independent install path option
        self.targetInstallPath['0.9.6'] = 'bin'

from Source.FileSource import *
from Package.PackageBase import *
from BuildSystem.BinaryBuildSystem import *

class Package( PackageBase, FileSource, BinaryBuildSystem ):
    def __init__( self ):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        self.subinfo.options.install.installPath = "bin"
        FileSource.__init__( self )
        PackageBase.__init__( self )
        BinaryBuildSystem.__init__( self )

if __name__ == '__main__':
    Package().execute()
