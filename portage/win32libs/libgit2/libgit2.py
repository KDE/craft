# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/libgit2/libgit2.git'

        self.description = "a portable C library for accessing git repositories"
        self.defaultTarget = 'master'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

# self.subinfo.options.configure.args = "-DDBUS_REPLACE_LOCAL_DIR=ON "
