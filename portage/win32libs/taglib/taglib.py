import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs/zlib'] = 'default'
        self.shortDescriptions = "audio meta-data library"

    def setTargets( self ):
        self.targets["1.8"] = 'http://github.com/downloads/taglib/taglib/taglib-1.8.tar.gz'
        self.targetInstSrc["1.8"] = 'taglib-1.8'
        self.patchToApply['1.8'] = [("taglib-1.8-20130307.diff", 1)]
        self.targetDigests['1.8'] = 'bdbfd746fde42401d3a77cd930c7802d374a692d'
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/taglib'
        self.shortDescription = "audio metadata library"
        self.defaultTarget = '1.8'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = ""
#        self.subinfo.options.configure.defines += " -DBUILD_TESTS=ON"
#        self.subinfo.options.configure.defines += " -DBUILD_EXAMPLES=ON"
#        self.subinfo.options.configure.defines += " -DNO_ITUNES_HACKS=ON"
        self.subinfo.options.configure.defines += " -DWITH_ASF=ON"
        self.subinfo.options.configure.defines += " -DWITH_MP4=ON"

