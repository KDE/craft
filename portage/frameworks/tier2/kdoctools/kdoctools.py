import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues(patchLevel=1)
        self.patchToApply["5.33.0-1"] = [("0001-Solve-a-visibility-conflict-for-meinproc5.patch", 1)]
        self.shortDescription = "Documentation generation from docbook "


    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.dependencies["libs/qtbase"] = "default"
        self.dependencies["frameworks/karchive"] = "default"
        self.dependencies["frameworks/ki18n"] = "default"
        self.dependencies["win32libs/libxslt"] = "default"
        self.dependencies["data/docbook-dtd"] = "default"
        self.dependencies["data/docbook-xsl"] = "default"
        
from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )
        # this package is currently not portable due to hardcoded path in the xml files
        self.subinfo.options.package.disableBinaryCache = True


    

