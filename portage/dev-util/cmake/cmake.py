import info


class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['3.0.0'] = 'http://www.cmake.org/files/v3.0/cmake-3.0.0-win32-x86.zip'
        self.targetMergeSourcePath['3.0.0'] = 'cmake-3.0.0-win32-x86'

        self.shortDescription = "CMake, the cross-platform, open-source build system."
        self.homepage = "http://www.cmake.org/"

        self.defaultTarget = '3.0.0'


    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base']       = 'default'
        self.buildDependencies['gnuwin32/patch'] = 'default'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.merge.destinationPath = "dev-utils"
        self.subinfo.options.merge.ignoreBuildType = True

