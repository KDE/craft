import info
import EmergeHash

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ['3.2.1', '3.2.2', '3.2.3', '3.3.1', '3.4.1']:
            self.targets[ver] = 'http://www.cmake.org/files/v%s/cmake-%s-win32-x86.zip' % (ver[:3], ver)
            self.targetMergeSourcePath[ver] = 'cmake-%s-win32-x86' % ver
            self.targetDigestUrls[ver] = ("https://cmake.org/files/v%s/cmake-%s-SHA-256.txt"% (ver[:3], ver), EmergeHash.HashAlgorithm.SHA256)

        nightlyUrl = "https://cmake.org/files/dev/"
        nightlyVer = utils.UtilsCache.getNightlyVersionsFromUrl(nightlyUrl + "?C=M;O=D;F=0", "\d.\d.\d\d\d\d\d\d\d\d-[0-9A-Za-z]{5,8}" + re.escape("-win32-x86"))[0]
        self.targets["gitHEAD"] = "%s/cmake-%s.zip" %(nightlyUrl, nightlyVer)
        self.targetMergeSourcePath["gitHEAD"] = 'cmake-%s' % nightlyVer

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

