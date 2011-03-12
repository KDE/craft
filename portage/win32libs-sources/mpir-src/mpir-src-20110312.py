import os
from shells import MSysShell
import info


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        if compiler.isMinGW():
                self.buildDependencies['dev-util/msys'] = 'default'
        else:
                self.buildDependencies['dev-util/yasm'] = 'default'

    def setTargets( self ):
        self.targets['2.3.0'] = 'http://www.mpir.org/mpir-2.3.0.tar.bz2'
        self.targetInstSrc['2.3.0'] = "mpir-2.3.0"
        self.patchToApply['2.3.0'] = ('mpir-2.3.0-20110310.diff', 1)

        self.options.package.withCompiler = False
        self.shortDescription = "Library for arbitrary precision integer arithmetic derived from version 4.2.1 of gmp"
        self.defaultTarget = '2.3.0'

from Package.AutoToolsPackageBase import *
from Package.MakeFilePackageBase import *

class PackageMinGW(AutoToolsPackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        AutoToolsPackageBase.__init__(self)
        abi = "ABI=32"
        if self.buildArchitecture()=="x64":
            abi = "ABI=64"
        self.subinfo.options.configure.defines = "--enable-shared --disable-static --enable-gmpcompat --enable-cxx " + abi

class PackageMSVC(MakeFilePackageBase):
    def __init__( self, **args ):
            self.subinfo = subinfo()
            MakeFilePackageBase.__init__( self )
            
    def configure( self ):
        os.chdir( os.path.join( self.sourceDir(), 'build.vc10') )
        os.putenv('YASMPATH', os.path.join(self.rootdir, 'dev-utils', 'bin'))
        self.system("configure.bat --enable-shared --cpu-none --ABI32")
        return True

    def make( self ):
        os.chdir( os.path.join( self.sourceDir(), 'build.vc10') )
        self.system("make.bat")
        return True

    def install( self ):
        if not os.path.isdir( os.path.join( self.installDir() , "bin" ) ):
                os.makedirs( os.path.join( self.installDir() , "bin" ) )
        shutil.move(os.path.join( self.sourceDir(), 'build.vc10', 'dll', 'Win32', 'Release', 'mpir.dll'), os.path.join( self.installDir() , "bin" , "mpir.dll") )
        
        if not os.path.isdir( os.path.join( self.installDir() , "lib" ) ):
                os.makedirs( os.path.join( self.installDir() , "lib" ) )
        shutil.move(os.path.join( self.sourceDir(), 'build.vc10', 'dll', 'Win32', 'Release', 'mpir.lib'), os.path.join( self.installDir() , "lib" , "mpir.lib") )
        # a dirty workaround the fact that FindGMP.cmake will only look for gmp.lib
        shutil.copy(os.path.join( self.installDir() , "lib" , "mpir.lib"), os.path.join( self.installDir() , "lib" , "gmp.lib") )

        if not os.path.isdir( os.path.join( self.installDir() , "include" ) ):
                os.makedirs( os.path.join( self.installDir() , "include" ) )
        shutil.move(os.path.join( self.sourceDir(), 'build.vc10', 'dll', 'Win32', 'Release', 'gmp.h'), os.path.join( self.installDir() , "include" , "gmp.h") )
        shutil.move(os.path.join( self.sourceDir(), 'build.vc10', 'dll', 'Win32', 'Release', 'gmpxx.h'), os.path.join( self.installDir() , "include" , "gmpxx.h") )
        shutil.move(os.path.join( self.sourceDir(), 'build.vc10', 'dll', 'Win32', 'Release', 'mpir.h'), os.path.join( self.installDir() , "include" , "mpir.h") )
        shutil.move(os.path.join( self.sourceDir(), 'build.vc10', 'dll', 'Win32', 'Release', 'mpirxx.h'), os.path.join( self.installDir() , "include" , "mpirxx.h") )
        shutil.move(os.path.join( self.sourceDir(), 'build.vc10', 'dll', 'Win32', 'Release', 'gmp-mparam.h'), os.path.join( self.installDir() , "include" , "gmp-mparam.h") )
        
        return True

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
