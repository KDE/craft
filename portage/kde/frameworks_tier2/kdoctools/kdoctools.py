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

        self.shortDescription = "Documentation generation from docbook "
        self.defaultTarget = self.versionInfo.defaultTarget()

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
        CMakePackageBase.__init__( self )


    def install( self ):
        if not CMakePackageBase.install( self ):
            return False
        return True

