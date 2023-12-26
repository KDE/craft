# -*- coding: utf-8 -*-
import info
from Package.MSBuildPackageBase import *
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotMacOS

    def setTargets(self):
        for ver in ['1.15']:
            self.targets[ver] = 'https://ftp.gnu.org/pub/gnu/libiconv/libiconv-%s.tar.gz' % ver
            self.targetInstSrc[ver] = "libiconv-%s" % ver
        self.targetDigests['1.15'] = (['ccf536620a45458d26ba83887a983b96827001e92a13847b45e4925cc8913178'], CraftHash.HashAlgorithm.SHA256)

        self.description = "GNU internationalization (i18n)"
        self.defaultTarget = '1.15'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += " --disable-static --enable-shared "
        self.subinfo.shelveAble = False
