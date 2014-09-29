import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "Qt 5 addon providing access to numerous types of archives"
        

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies["libs/qtbase"] = "default"
        self.dependencies["win32libs/libbzip2"] = "default"
        self.dependencies["win32libs/zlib"] = "default"
        if not compiler.isMSVC2010() and not compiler.isMSVC2012():
            self.dependencies["win32libs/liblzma"] = "default"

        for ver in ('5.0.0', '5.1.0', '5.2.0'):
            self.patchToApply[ver] = [('get-rid-of-VLAs.diff', 1)]

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

