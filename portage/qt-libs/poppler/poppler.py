# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "git://git.freedesktop.org/git/poppler/poppler"
        for ver in ["0.38.0", "0.57.0"]:
            self.targets[ver] = f"http://poppler.freedesktop.org/poppler-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"poppler-{ver}"
        self.patchToApply["0.38.0"] = ("poppler-0.38.0-20151130.diff", 1)
        self.patchToApply["0.57.0"] = ("poppler-0.57.0-20170810.diff", 1)
        self.targetDigests["0.38.0"] = "62d334116e509d59cd1d8f172f02c0a81e73182f"
        self.targetDigests['0.57.0'] = (
            ['0ea37de71b7db78212ebc79df59f99b66409a29c2eac4d882dae9f2397fe44d8'], CraftHash.HashAlgorithm.SHA256)

        self.description = "PDF rendering library based on xpdf-3.0"
        self.defaultTarget = "0.57.0"

    def setDependencies(self):
        self.buildDependencies["dev-util/pkg-config"] = "default"
        self.runtimeDependencies["data/poppler-data"] = "default"
        self.runtimeDependencies["win32libs/freetype"] = "default"
        self.runtimeDependencies["win32libs/libjpeg-turbo"] = "default"
        self.runtimeDependencies["win32libs/lcms"] = "default"
        self.runtimeDependencies["win32libs/zlib"] = "default"
        self.runtimeDependencies["win32libs/openjpeg"] = "default"
        self.runtimeDependencies["win32libs/libjpeg-turbo"] = "default"
        self.runtimeDependencies["win32libs/libpng"] = "default"
        self.runtimeDependencies["win32libs/libcurl"] = "default"
        self.runtimeDependencies["win32libs/tiff"] = "default"
        self.runtimeDependencies["win32libs/win_iconv"] = "default"
        self.runtimeDependencies["data/poppler-data"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

        self.subinfo.options.package.packageName = "poppler"
        self.subinfo.options.configure.args = "-DENABLE_XPDF_HEADERS=ON -DENABLE_ZLIB=ON -DENABLE_LIBCURL=ON -DENABLE_UTILS=OFF -DENABLE_LIBOPENJPEG=openjpeg2"
