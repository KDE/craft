import info
import emergePlatform

class subinfo(info.infoclass):
    def setTargets( self ):
        if emergePlatform.buildArchitecture() == 'x64':
           self.targets['1.1.0'] = "http://www.tortall.net/projects/yasm/releases/vsyasm-1.1.0-win64.zip"
        else:
           self.targets['1.1.0'] = "http://www.tortall.net/projects/yasm/releases/vsyasm-1.1.0-win32.zip"
        self.shortDescription = "The Yasm Modular Assembler Project"
        self.defaultTarget = '1.1.0'
    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        ## @todo remove the readme.txt file
        self.subinfo.options.merge.destinationPath = "dev-utils/bin"
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
