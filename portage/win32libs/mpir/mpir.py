import os

import info

import utils


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['2.7.0-alpha10']:
            self.targets[ver] = 'http://www.mpir.org/mpir-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = "mpir-" + ver
        self.targetDigests['2.6.0'] = '28a91eb4d2315a9a73dc39771acf2b99838b9d72'
        self.patchToApply['2.6.0'] = ('mpir-2.6.0-20131003.diff', 1)
        self.targetDigests['2.7.0-alpha10'] = '815fee928c9ba5f444457144dd037300cb8f4ca4'
        self.targetInstSrc['2.7.0-alpha10'] = 'mpir-2.7.0'

        self.shortDescription = "Library for arbitrary precision integer arithmetic derived from version 4.2.1 of gmp"
        self.defaultTarget = '2.7.0-alpha10'

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
        os.chdir( os.path.join( self.sourceDir(), 'build.vc12') )
        os.putenv('YASMPATH', os.path.join(self.rootdir, 'dev-utils', 'bin'))
        return True

    def make( self ):
        os.chdir( os.path.join( self.sourceDir(), 'build.vc12') )
        if self.buildType() == "Debug":
            bt = "Debug"
        else:
            bt = "Release"

        toolsetSwitches = ""
        if compiler.isMSVC2012():
            toolsetSwitches = "/property:PlatformToolset=v110"
        elif compiler.isMSVC2013():
            toolsetSwitches = "/tv:12.0 /property:PlatformToolset=v120"

        return utils.system("msbuild /target:lib_mpir_gc \"%s\" /p:Configuration=%s %s" %
                (os.path.join(self.sourceDir(), "build.vc12", "mpir.sln"), bt, toolsetSwitches)
        ) and utils.system("msbuild /target:dll_mpir_gc \"%s\" /p:Configuration=%s %s" %
                (os.path.join(self.sourceDir(), "build.vc12", "mpir.sln"), bt, toolsetSwitches)
        )

    def install( self ):
        if not os.path.isdir( os.path.join( self.installDir() , "bin" ) ):
                os.makedirs( os.path.join( self.installDir() , "bin" ) )
        utils.copyFile(os.path.join( self.sourceDir(), 'dll', 'Win32', 'Release', 'mpir.dll'), os.path.join( self.installDir() , "bin" , "mpir.dll") )
        
        if not os.path.isdir( os.path.join( self.installDir() , "lib" ) ):
                os.makedirs( os.path.join( self.installDir() , "lib" ) )
        utils.copyFile(os.path.join( self.sourceDir(), 'dll', 'Win32', 'Release', 'mpir.lib'), os.path.join( self.installDir() , "lib" , "mpir.lib") )
        # a dirty workaround the fact that FindGMP.cmake will only look for gmp.lib
        utils.copyFile(os.path.join( self.installDir() , "lib" , "mpir.lib"), os.path.join( self.installDir() , "lib" , "gmp.lib") )

        if not os.path.isdir( os.path.join( self.installDir() , "include" ) ):
                os.makedirs( os.path.join( self.installDir() , "include" ) )
        utils.copyFile(os.path.join( self.sourceDir(), 'dll', 'Win32', 'Release', 'gmp.h'), os.path.join( self.installDir() , "include" , "gmp.h") )
        utils.copyFile(os.path.join( self.sourceDir(), 'dll', 'Win32', 'Release', 'gmpxx.h'), os.path.join( self.installDir() , "include" , "gmpxx.h") )
        utils.copyFile(os.path.join( self.sourceDir(), 'dll', 'Win32', 'Release', 'mpir.h'), os.path.join( self.installDir() , "include" , "mpir.h") )
        utils.copyFile(os.path.join( self.sourceDir(), 'dll', 'Win32', 'Release', 'mpirxx.h'), os.path.join( self.installDir() , "include" , "mpirxx.h") )
        utils.copyFile(os.path.join( self.sourceDir(), 'dll', 'Win32', 'Release', 'gmp-mparam.h'), os.path.join( self.installDir() , "include" , "gmp-mparam.h") )
        
        return True

if compiler.isMinGW():
    class Package(PackageMinGW):
        def __init__( self ):
            PackageMinGW.__init__( self )
else:
    class Package(PackageMSVC):
        def __init__( self ):
            PackageMSVC.__init__( self )

