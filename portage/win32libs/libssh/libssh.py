# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in [(195, '0.7.3')]:
            # e.g. https://red.libssh.org/attachments/download/195/libssh-0.7.3.tar.xz
            self.targets[ver[1]] = "https://red.libssh.org/attachments/download/{0}/libssh-{1}.tar.xz".format(ver[0],
                                                                                                              ver[1])
            self.targetInstSrc[ver[1]] = "libssh-" + ver[1]
        self.targetDigests['0.7.3'] = '9de2a8fde51aa7b7855008fafd5bf47ebb01289f'

        self.svnTargets['master'] = "git://git.libssh.org/projects/libssh.git"

        self.description = "a working SSH implementation by the mean of a library"
        self.defaultTarget = '0.7.3'
        # self.options.configure.args = "-DWITH_STATIC_LIB=ON"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["win32libs/zlib"] = "default"
        self.runtimeDependencies["win32libs/openssl"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
