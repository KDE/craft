# -*- coding: utf-8 -*-
import info
import utils
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
       for ver in [ '7.19.6' ,'7.20.0', '7.28.1' ]:
          self.targets[ver] = 'http://curl.haxx.se/download/curl-' + ver + '.tar.bz2'
          self.targetInstSrc[ver] = 'curl-' + ver
       self.patchToApply['7.20.0'] = ("7.20.0.diff", 1)
       self.patchToApply['7.28.1'] = [("curl-7.28.1-20130202.diff", 1), ("curl-7.28.1-installlocation.diff", 1)]
       self.targetDigests['7.28.1'] = 'b5aff1afc4e40fcb78db7a5e27214e0035756f3d'
       self.shortDescription = "a free and easy-to-use client-side URL transfer library"
       self.defaultTarget = '7.20.0'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = " -DBUILD_CURL_TESTS=OFF"

    def unpack(self):
        if not CMakePackageBase.unpack( self ):
            return False
        if(self.subinfo.buildTarget in ['7.20.0', '7.28.1']):
          return True
        # we have an own cmake script - copy it to the right place
        cmake_script = os.path.join( self.packageDir() , "CMakeLists.txt" )
        cmake_dest = os.path.join( self.sourceDir() , "CMakeLists.txt" )
        shutil.copy( cmake_script, cmake_dest )
        return True


if __name__ == '__main__':
    Package().execute()

