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
        if COMPILER == "msvc2008":
            self.subinfo.options.package.version = '9.0.30729.1'
        elif COMPILER == "mingw4":
            self.subinfo.options.package.version = '4.4.0'
        

    def fetch(self):
        return True

    def unpack(self):
        destdir = os.path.join(self.installDir(),"bin")
        utils.createDir(self.workDir())
        utils.createDir(destdir)
        if COMPILER == "msvc2008":
            if self.buildType() == "Debug":
                srcdir = os.path.join(self.packageDir(),"redist","Debug_NonRedist","x86","Microsoft.VC90.DebugCRT")
                files = [ "Microsoft.VC90.DebugCRT.manifest", "msvcr90d.dll", "msvcp90d.dll", "msvcm90d.dll"]
            else:
                srcdir = os.path.join(self.packageDir(),"redist","x86","Microsoft.VC90.CRT")
                files = [ "Microsoft.VC90.CRT.manifest", "msvcr90.dll", "msvcp90.dll", "msvcm90.dll"]
        elif COMPILER == "mingw4":
            srcdir = os.path.join(self.rootdir,"mingw","bin")
            files = ['mingwm10.dll','libgcc_s_dw2-1.dll']
        
        # todo do other compiler mingw_w32,  mingw_w64 need similar runtime files ? 

        for file in files:
            utils.copyFile(os.path.join(srcdir,file), os.path.join(destdir,file))
            
        return True

if __name__ == '__main__':
    Package().execute()
