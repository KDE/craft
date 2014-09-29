import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues()
        self.shortDescription = "Documentation generation from docbook "


    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies["libs/qtbase"] = "default"
        self.dependencies["frameworks/karchive"] = "default"
        self.dependencies["win32libs/libxslt"] = "default"
        self.dependencies["data/docbook-dtd"] = "default"
        self.dependencies["data/docbook-xsl"] = "default"
        
from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

