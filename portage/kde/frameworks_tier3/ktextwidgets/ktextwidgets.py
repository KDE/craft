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

        self.shortDescription = "KTextWidgets provides widgets for displaying and editing text"
        self.defaultTarget = self.versionInfo.defaultTarget()

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.buildDependencies["win32libs/automoc"] = "default"
        self.dependencies["kde/kcompletion"] = "default"
        self.dependencies["kde/kconfig"] = "default"
        self.dependencies["kde/kconfigwidgets"] = "default"
        self.dependencies["kde/ki18n"] = "default"
        self.dependencies["kde/kiconthemes"] = "default"
        self.dependencies["kde/kservice"] = "default"
        self.dependencies["kde/kwidgetsaddons"] = "default"
        self.dependencies["kde/kwindowsystem"] = "default"
        self.dependencies["kde/sonnet"] = "default"

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

