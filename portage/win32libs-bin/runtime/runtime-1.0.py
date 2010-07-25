import info

class subinfo(info.infoclass):
    def setTargets( self ):
        # not used  yet only for reference
        self.targets['vc90-9.0.21022.8'] = "http://download.microsoft.com/download/1/1/1/1116b75a-9ec3-481a-a3c8-1777b5381140/vcredist_x86.exe"
        self.defaultTarget = 'vc90-9.0.21022.8'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

from Package.BinaryPackageBase import *
        
class Package(BinaryPackageBase):
    def __init__(self):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__( self )
        self.subinfo.options.package.version = '9.0.21022.8'
        if os.getenv( "KDECOMPILER" ) <> "msvc2008":
            utils.die("this package is currently indented only for msvc 2008 compilers")

    def fetch(self):
        return True

    def unpack(self):
        destdir = os.path.join(self.installDir(),"bin")
        utils.createDir(self.workDir())
        utils.createDir(destdir)
        for file in [ "Microsoft.VC90.CRT.manifest", "msvcr90.dll", "msvcp90.dll", "msvcm90.dll"]:
            utils.copyFile(os.path.join(self.packageDir(),file), os.path.join(destdir,file))
        return True

if __name__ == '__main__':
    Package().execute()
