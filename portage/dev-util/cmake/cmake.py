import info


class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ['3.2.1', '3.2.2', '3.2.3', '3.3.1', '3.4.1']:
            self.targets[ver] = 'http://www.cmake.org/files/v%s/cmake-%s-win32-x86.zip' % (ver[:3], ver)
            self.targetMergeSourcePath[ver] = 'cmake-%s-win32-x86' % ver
        self.targetDigests['3.2.1'] = '4011f4f18c002a9ff97c76ea1d397eca9b675f98'
        self.targetDigests['3.2.3'] = 'de3acd4c99057584bb2d149a982eca47caad8e22'
        self.targetDigests['3.3.1'] = 'cbe93de9e5861c8b0b441d5c40fb68b9b27ac7af'
        self.targetDigests['3.4.1'] = '4894baeafc0368d6530bf2c6bfe4fc94056bd04a'

        nightlyUrl = "https://cmake.org/files/dev/"
        nightlyVer = utils.getNightlyVersionsFromUrl(nightlyUrl + "?C=M;O=D", "\d.\d.\d\d\d\d\d\d\d\d-[0-9A-Za-z]{5,8}")[0]
        self.targets["gitHEAD"] = "%s/cmake-%s-win32-x86.zip" %(nightlyUrl, nightlyVer)
        self.targetMergeSourcePath["gitHEAD"] = 'cmake-%s-win32-x86' % nightlyVer

        self.shortDescription = "CMake, the cross-platform, open-source build system."
        self.homepage = "http://www.cmake.org/"

        self.defaultTarget = '3.4.1'


    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base']       = 'default'
        self.buildDependencies['gnuwin32/patch'] = 'default'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.merge.destinationPath = "dev-utils"
        self.subinfo.options.merge.ignoreBuildType = True

