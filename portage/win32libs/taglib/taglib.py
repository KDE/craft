import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs/zlib'] = 'default'
        self.shortDescriptions = "audio meta-data library"

    def setTargets( self ):
        self.targets["1.9.1"] = 'https://taglib.github.io/releases/taglib-1.9.1.tar.gz'
        self.targetInstSrc["1.9.1"] = 'taglib-1.9.1'
        self.patchToApply['1.9.1'] = [("dont-export-filename.diff", 1)]
        self.targetDigests['1.9.1'] = '4fa426c453297e62c1d1eff64a46e76ed8bebb45'
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/taglib'
        self.shortDescription = "audio metadata library"
        self.defaultTarget = '1.9.1'

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

