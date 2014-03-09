import info
import kdedefaults as kd

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets["gitHEAD"] = "[git]kde:%s|%s|" % (self.package, kd.kdebranch)
        self.shortDescription = "KConfig"
        self.defaultTarget = "gitHEAD"

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.buildDependencies["win32libs/automoc"] = "default"
        self.dependencies["libs/qtbase"] = "default"
from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = ""
        if compiler.isMinGW():
          self.subinfo.options.configure.defines += " -DKDE_DISTRIBUTION_TEXT=\"MinGW %s\" " % compiler.getMinGWVersion()
        elif compiler.isMSVC():
          self.subinfo.options.configure.defines = " -DKDE_DISTRIBUTION_TEXT=\"%s\" " % compiler.getVersion()

    def install( self ):
        if not CMakePackageBase.install( self ):
            return False
        return True

if __name__ == "__main__":
    Package().execute()
