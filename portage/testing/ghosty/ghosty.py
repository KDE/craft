import info
import compiler

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs/zlib'] = 'default'

    def setTargets( self ):
        for ver in ['9.18']:
            self.targets[ ver ] = "http://downloads.ghostscript.com/public/ghostscript-" + ver + ".tar.gz"
            self.targetInstSrc[ ver ] = "ghostscript-" + ver
        self.targetDigests['9.18'] = '761c9c25b9f5fe01197bd1510f527b3c1b6eb9de'
        self.defaultTarget = '9.18'

from Package.CMakePackageBase import *

class PackageMSVC(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )

    def configure( self ):
        return True

    def make( self ):
        self.enterSourceDir()
        _win64 = ""
        if compiler.isX64(): _win64 = " WIN64="
        self.system( "nmake -f psi\\msvc.mak" + _win64 )
        return True

    def install( self ):
        src = self.sourceDir()
        dst = self.imageDir()

        if not os.path.isdir(dst):
            os.mkdir(dst)
        if not os.path.isdir(os.path.join(dst, "bin")):
            os.mkdir(os.path.join(dst, "bin"))
        if not os.path.isdir(os.path.join(dst, "lib")):
            os.mkdir(os.path.join(dst, "lib"))
        if not os.path.isdir(os.path.join(dst, "include")):
            os.mkdir(os.path.join(dst, "include"))
        if not os.path.isdir(os.path.join(dst, "include", "ghostscript")):
            os.mkdir(os.path.join(dst, "include", "ghostscript"))

        if compiler.isX64():
            shutil.copy(os.path.join(src, "bin", "gsdll64.dll"), os.path.join(dst, "bin"))
            shutil.copy(os.path.join(src, "bin", "gsdll64.lib"), os.path.join(dst, "lib"))
        else:
            shutil.copy(os.path.join(src, "bin", "gsdll32.dll"), os.path.join(dst, "bin"))
            shutil.copy(os.path.join(src, "bin", "gsdll32.lib"), os.path.join(dst, "lib"))
        shutil.copy(os.path.join(src, "bin", "gswin64.exe"), os.path.join(dst, "bin"))
        shutil.copy(os.path.join(src, "bin", "gswin64c.exe"), os.path.join(dst, "bin"))
        shutil.copy(os.path.join(src, "psi", "iapi.h"), os.path.join(dst, "include", "ghostscript"))
        shutil.copy(os.path.join(src, "psi", "ierrors.h"), os.path.join(dst, "include", "ghostscript"))
        shutil.copy(os.path.join(src, "devices", "gdevdsp.h"), os.path.join(dst, "include", "ghostscript"))
        shutil.copy(os.path.join(src, "base", "gserrors.h"), os.path.join(dst, "include", "ghostscript"))
        utils.copySrcDirToDestDir(os.path.join(src, "lib"), os.path.join(dst, "lib"))

        return True

from Package.AutoToolsPackageBase import *

class PackageMSys(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.make.supportsMultijob = False
        self.subinfo.options.package.packageName = 'ghostscript'
        self.subinfo.options.package.packSources = False
        if compiler.architecture() == "x64":
            self.platform = "mingw64"
        else:
            self.platform = "mingw"
        self.supportsCCACHE = False

        self.buildInSource = True

if compiler.isMinGW():
    class Package(PackageMSys): pass
else:
    class Package(PackageMSVC): pass