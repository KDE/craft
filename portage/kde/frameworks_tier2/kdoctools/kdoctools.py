import info
import kdedefaults as kd
from emerge_config import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets["gitHEAD"] = "[git]kde:%s|%s|" % (self.package, kd.kdebranch)
        self.shortDescription = "Documentation generation from docbook "
        self.defaultTarget = "gitHEAD"

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies["libs/qtbase"] = "default"
        self.dependencies["kde/karchive"] = "default"
        self.dependencies["win32libs/libxslt"] = "default"
        self.dependencies["data/docbook-dtd"] = "default"
        self.dependencies["data/docbook-xsl"] = "default"
        
from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )


    def install( self ):
        if not CMakePackageBase.install( self ):
            return False
        return True

if __name__ == "__main__":
    Package().execute()
