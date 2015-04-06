import info


class subinfo( info.infoclass ):
    def setTargets( self ):
        ver = '3.2.1'
        self.targets[ver] = 'http://www.cmake.org/files/v3.2/cmake-%s-win32-x86.zip' % ver
        self.targetMergeSourcePath[ver] = 'cmake-%s-win32-x86' % ver
        self.targetDigests['3.2.1'] = '4011f4f18c002a9ff97c76ea1d397eca9b675f98'
        
        self.shortDescription = "CMake, the cross-platform, open-source build system."
        self.homepage = "http://www.cmake.org/"

        self.defaultTarget = '3.2.1'


    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base']       = 'default'
        self.buildDependencies['gnuwin32/patch'] = 'default'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.merge.destinationPath = "dev-utils"
        self.subinfo.options.merge.ignoreBuildType = True

