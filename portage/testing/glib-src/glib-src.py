from Package.CMakePackageBase import *
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets["2.29.14"] = "http://ftp.acc.umu.se/pub/GNOME/sources/glib/2.29/glib-2.29.14.tar.bz2"
        self.targetInstSrc["2.29.14"] = "glib-2.29.14"
        self.targets["2.36.3"] = "http://ftp.acc.umu.se/pub/GNOME/sources/glib/2.36/glib-2.36.3.tar.xz"
        self.targetDigests['2.36.3'] = 'aafba69934b9ba77cc8cb0e5d8105aa1d8463eba'
        self.targetInstSrc["2.36.3"] = "glib-2.36.3"
        if compiler.isMSVC():
            self.patchToApply["2.29.14"] = ('glib-2.29.14-20121010.diff', 1)
            self.patchToApply["2.36.3"] = ('glib-2.29.14-20121010.diff', 1)
        else:
            self.patchToApply["2.36.3"] = [('glib-2.36.3-20130624_mingw.diff',1),
                                           ('0001-Fix-compiling-for-win64.patch',1)]
        self.defaultTarget = "2.36.3"
        self.shortDescription = "The Glib libraries: glib, gio, gthread, gmodule, gobject"
        

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'        
        self.buildDependencies['dev-util/pkg-config'] = 'default'
        self.dependencies['testing/libffi-src'] = 'default'
        self.dependencies['win32libs/gettext'] = 'default'
            


class PackageMSVC(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__( self )

    def configure( self ):
        return True

    def make( self ):
        return True

    def compile( self ):
        self.enterSourceDir()
        os.putenv( "INSTALLDIR", self.imageDir() )
        configuration = "Release"
        if self.buildType() == "Debug":
            configuration = "Debug"
        platform = "Win32"
        if self.buildArchitecture() == "x64":
            platform = "x64"
        cmd = "msbuild /p:configuration=\""+configuration+"\" /p:platform=\""+platform+"\" build\\win32\\vs10\\glib.sln"
        return self.system( cmd )

    def install( self ):
        self.enterSourceDir()
        os.putenv( "INSTALLDIR", self.imageDir() )
        configuration = "Release"
        if self.buildType() == "Debug":
            configuration = "Debug"
        platform = "Win32"
        if self.buildArchitecture() == "x64":
            platform = "x64"
        cmd = "msbuild /p:configuration=\""+configuration+"\" /p:platform=\""+platform+"\" /t:install build\\win32\\vs10\\glib.sln"
        return self.system( cmd )

from Package.AutoToolsPackageBase import *

class PackageMinGW( AutoToolsPackageBase):
    def __init__( self ):
        if not self.subinfo.options.features.msys2:
            utils.die("Glib requries the msys2 feature activated to compile")
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.defines = " --enable-gtk-doc=no --enable-static=no --enable-shared=yes --disable-modular-tests"


        
if compiler.isMinGW():
    class Package(PackageMinGW):
        def __init__( self ):
            PackageMinGW.__init__( self )
else:
    class Package(PackageMSVC):
        def __init__( self ):
            PackageMSVC.__init__( self )

if __name__ == '__main__':
    Package().execute()
