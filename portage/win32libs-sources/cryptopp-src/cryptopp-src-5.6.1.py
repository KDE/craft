import base
import os
import shutil
import utils
import info
import emergePlatform

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets[ '561' ] = 'http://www.cryptopp.com/cryptopp561.zip'  
        self.patchToApply[ '561' ] = ('cmake.diff', 1)        
        self.targetDigests['561'] = '31dbb456c21f50865218c57b7eaf4c955a222ba1'       
        self.shortDescription = "Crypto++ Library is a free C++ class library of cryptographic schemes"
        self.defaultTarget = '561'


    def setDependencies( self ):
            self.buildDependencies['virtual/base'] = 'default'
            if compiler.isMinGW():
                self.buildDependencies['dev-util/msys'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = False


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = "-DCRYPTOPP_BUILD_SHARED_LIBS=OFF -DCRYPTOPP_BUILD_TESTS=OFF"
         
        

if __name__ == '__main__':
      Package().execute()

