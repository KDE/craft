import info
import kdedefaults as kd
from emerge_config import *

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in self.versionInfo.tarballs():
            self.targets[ver] = "http://download.kde.org/unstable/frameworks/%s/%s-%s.tar.xz" % ( ver, self.package, ver )
            self.targetDigestUrls[ver] = "http://download.kde.org/unstable/frameworks/%s/%s-%s.tar.xz.sha1" % (ver, self.package, ver)
            self.targetInstSrc[ver] = "%s-%s" % ( self.package, ver)

        for ver in self.versionInfo.branches():
            self.svnTargets[ver] = "[git]kde:%s|%s|" % (self.package, ver)

        for ver in self.versionInfo.tags():
            self.svnTargets[ver] = "[git]kde:%s||%s" % (self.package, ver)

        self.shortDescription = "Extra widgets for easier configuration support"
        self.defaultTarget = self.versionInfo.defaultTarget()

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.buildDependencies["win32libs/automoc"] = "default"
        self.buildDependencies["kde/kauth"] = "default"
        self.buildDependencies["kde/kcoreaddons"] = "default"
        self.buildDependencies["kde/kcodecs"] = "default"
        self.buildDependencies["kde/kconfig"] = "default"
        self.buildDependencies["kde/kdoctools"] = "default"
        self.buildDependencies["kde/kguiaddons"] = "default"
        self.buildDependencies["kde/ki18n"] = "default"
        self.buildDependencies["kde/kwidgetsaddons"] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = ""
        if compiler.isMinGW():
          self.subinfo.options.configure.defines += " -DKDE_DISTRIBUTION_TEXT=\"MinGW %s\" " % compiler.getMinGWVersion()
        elif compiler.isMSVC():
          self.subinfo.options.configure.defines += " -DKDE_DISTRIBUTION_TEXT=\"%s\" " % compiler.getVersion()

    def install( self ):
        if not CMakePackageBase.install( self ):
            return False
        return True

