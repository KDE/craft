import info


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["win32libs/boost/boost-thread"] = "default"
        self.runtimeDependencies["win32libs/boost/boost-system"] = "default"
        self.runtimeDependencies["win32libs/boost/boost-regex"] = "default"
        self.runtimeDependencies["win32libs/boost/boost-iostreams"] = "default"
        self.runtimeDependencies["win32libs/boost/boost-date-time"] = "default"
        self.runtimeDependencies["win32libs/boost/boost-filesystem"] = "default"
        self.runtimeDependencies["win32libs/boost/boost-atomic"] = "default"

    def setTargets(self):
        for ver in []:
            self.targets[ver] = "https://github.com/luceneplusplus/LucenePlusPlus/archive/rel_%s.tar.gz" % ver
            self.archiveNames[ver] = "luceneplusplus-%s.tar.gz" % ver
            self.targetInstSrc[ver] = "LucenePlusPlus-rel_%s" % ver
        self.patchToApply["master"] = ("luceneplusplus-20150916.patch", 1)

        self.svnTargets["master"] = "https://github.com/luceneplusplus/LucenePlusPlus.git"

        self.description = "Lucene++ is an up to date C++ port of the popular Java Lucene library, a high-performance, full-featured text search engine."
        self.webpage = "https://github.com/luceneplusplus/LucenePlusPlus/"
        self.defaultTarget = "master"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DENABLE_TEST=OFF -DENABLE_DEMO=OFF"
