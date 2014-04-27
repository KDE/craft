import os

import info


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['2.3.0', '2.5.0', '2.6.0']:
            self.targets[ver] = 'http://www.mpir.org/mpir-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = "mpir-" + ver
        self.targetDigests['2.3.0'] = 'e359e8d7417e4ffef40ba975409c306ac4c381e5'
        self.patchToApply['2.3.0'] = ('mpir-2.3.0-20110310.diff', 1)
        self.targetDigests['2.5.0'] = 'de6adf9c5318dfba52b29d1700812069cfb6be39'
        self.patchToApply['2.5.0'] = ('mpir-2.5.0-20120201.diff', 1)
        self.targetDigests['2.6.0'] = '28a91eb4d2315a9a73dc39771acf2b99838b9d72'
        self.patchToApply['2.6.0'] = ('mpir-2.6.0-20131003.diff', 1)

        self.shortDescription = "Library for arbitrary precision integer arithmetic derived from version 4.2.1 of gmp"
        self.defaultTarget = '2.6.0'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        if compiler.isMinGW():
                self.buildDependencies['dev-util/msys'] = 'default'
        else:
                self.buildDependencies['dev-util/yasm'] = 'default'

from Package.AutoToolsPackageBase import *
from Package.MakeFilePackageBase import *

class PackageMinGW(AutoToolsPackageBase):
    def __init__( self, **args ):
        AutoToolsPackageBase.__init__(self)
        abi = "ABI=64"
        if self.buildArchitecture()=="x86":
            abi = "ABI=32"
            self.platform = ""
        self.subinfo.options.configure.defines = "--enable-shared --disable-static --enable-gmpcompat --enable-cxx " + abi

class PackageMSVC(MakeFilePackageBase):
    def __init__( self, **args ):
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
