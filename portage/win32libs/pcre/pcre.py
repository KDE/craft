import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["8.41"]:
            self.targets[ver] = f"ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"pcre-{ver}"
        self.patchToApply["8.41"] = [("pcre-8.10-20101125.diff", 1)]
        self.targetDigests['8.41'] = (
            ['e62c7eac5ae7c0e7286db61ff82912e1c0b7a0c13706616e94a7dd729321b530'], CraftHash.HashAlgorithm.SHA256)

        self.description = "Perl-Compatible Regular Expressions"
        self.defaultTarget = "8.41"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        self.runtimeDependencies["win32libs/libbzip2"] = "default"
        self.runtimeDependencies["win32libs/zlib"] = "default"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

        defines = "-DBUILD_SHARED_LIBS=ON "
        defines += "-DPCRE_SUPPORT_UNICODE_PROPERTIES=ON "
        defines += "-DPCRE_SUPPORT_UTF8=ON "
        defines += "-DPCRE_EBCDIC=OFF "
        self.subinfo.options.configure.args = defines
