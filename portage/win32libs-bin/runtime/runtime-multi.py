import info

class subinfo(info.infoclass):
    def setTargets( self ):
        # not used  yet only for reference
        self.targets['vc90-9.0.21022.8'] = "http://download.microsoft.com/download/1/1/1/1116b75a-9ec3-481a-a3c8-1777b5381140/vcredist_x86.exe"
        self.defaultTarget = 'vc90-9.0.21022.8'

    def setDependencies( self ):
        self.hardDependencies['virtual/bin-base'] = 'default'

from Package.BinaryPackageBase import *
import compiler  
    
    
class Package(BinaryPackageBase):
    def __init__(self):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__( self )
        if compiler.isMSVC2008():
            self.subinfo.options.package.version = '9.0.30729.1'
        elif compiler.isMinGW32():
            self.subinfo.options.package.version = '4.4.0'
        elif compiler.isMinGW_WXX():
            self.subinfo.options.package.version = '4.4.5'
        

    def fetch(self):
        return True

    def unpack(self):
        destdir = os.path.join(self.installDir(),"bin")
        utils.createDir(self.workDir())
        utils.createDir(destdir)
        if compiler.isMSVC2008():
            if self.buildType() == "Debug":
                srcdir = os.path.join(self.packageDir(),"redist","Debug_NonRedist","x86","Microsoft.VC90.DebugCRT")
                files = [ "Microsoft.VC90.DebugCRT.manifest", "msvcr90d.dll", "msvcp90d.dll", "msvcm90d.dll"]
            else:
                srcdir = os.path.join(self.packageDir(),"redist","x86","Microsoft.VC90.CRT")
                files = [ "Microsoft.VC90.CRT.manifest", "msvcr90.dll", "msvcp90.dll", "msvcm90.dll"]
        elif compiler.isMinGW():
            if compiler.isMinGW32():
                srcdir = os.path.join(self.rootdir,"mingw","bin")
                files = ['mingwm10.dll','libgcc_s_dw2-1.dll']
            elif compiler.isMinGW_W32():
                srcdir = os.path.join(self.rootdir,"mingw","bin")
                files = ['libgcc_s_sjlj-1.dll']
            elif compler.isMinGW_W64():
                srcdir = os.path.join(self.rootdir,"mingw64","bin")
                files = ['libgcc_s_sjlj-1.dll']
        

        for file in files:
            utils.copyFile(os.path.join(srcdir,file), os.path.join(destdir,file))
            
        return True

if __name__ == '__main__':
    Package().execute()
