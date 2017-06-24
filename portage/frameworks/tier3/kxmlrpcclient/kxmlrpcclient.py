import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "This library contains simple XML-RPC Client support"
        self.patchToApply['5.33.0'] = [("fix-kxmlrpcclient.diff", 1)]

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["frameworks/ki18n"] = "default"
        self.runtimeDependencies["frameworks/kio"] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

