import info


class subinfo(info.infoclass):
    def setTargets( self ):
        if compiler.isX64():
            if compiler.isMinGW():
                self.targets['1.2.0'] = "http://www.tortall.net/projects/yasm/releases/yasm-1.2.0-win64.exe"
            if compiler.isMSVC():
                self.targets['1.2.0'] = "http://www.tortall.net/projects/yasm/releases/vsyasm-1.2.0-win64.zip"
        else:
            if compiler.isMinGW():
                self.targets['1.2.0'] = "http://www.tortall.net/projects/yasm/releases/yasm-1.2.0-win32.exe"
            if compiler.isMSVC():
                self.targets['1.2.0'] = "http://www.tortall.net/projects/yasm/releases/vsyasm-1.2.0-win32.zip"
        self.shortDescription = "The Yasm Modular Assembler Project"
        self.defaultTarget = '1.2.0'
    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        ## @todo remove the readme.txt file
        self.subinfo.options.merge.destinationPath = "dev-utils/bin"
        BinaryPackageBase.__init__(self)

    def install(self):
        if not BinaryPackageBase.install(self):
            return False
        if compiler.isMinGW_W32():
            shutil.move(os.path.join(self.imageDir(),"yasm-1.2.0-win32.exe"),os.path.join(self.imageDir(),"yasm.exe"))
        if compiler.isMinGW_W64():
            shutil.move(os.path.join(self.imageDir(),"yasm-1.2.0-win64.exe"),os.path.join(self.imageDir(),"yasm.exe"))
        return True


if __name__ == '__main__':
    Package().execute()
