# -*- coding: utf-8 -*-
from distutils.version import StrictVersion

import info


class subinfo(info.infoclass):
    def setTargets(self):
        versions = utils.utilsCache.getNightlyVersionsFromUrl("http://windows.php.net/downloads/releases",
                                                              re.compile(r"7\.\d\.\d\d"))
        versions.sort(key=lambda v: StrictVersion(v))
        for ver in versions:
            self.targets[ver] = "http://windows.php.net/downloads/releases/php-%s-Win32-VC14-%s.zip" % (
            ver, craftCompiler.architecture)
            self.targetDigestUrls[ver] = (
            "http://windows.php.net/downloads/releases/sha1sum.txt", CraftHash.HashAlgorithm.SHA1)
            self.targetInstallPath[ver] = os.path.join("dev-utils", "php")
            self.defaultTarget = ver


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def install(self):
        if not BinaryPackageBase.install(self):
            return False
        # TODO: ouch
        with open(os.path.join(self.imageDir(), "dev-utils", "php", "php.ini-development"), "rt+") as ini:
            with open(os.path.join(self.imageDir(), "dev-utils", "php", "php.ini"), "wt+") as out:
                ext_dir = re.compile("^; extension_dir = \"ext\".*$")
                curl = re.compile("^;extension=php_curl.dll.*$")
                for line in ini:
                    if ext_dir.match(line):
                        line = "extension_dir = \"ext\"\n"
                    elif curl.match(line):
                        line = "extension=php_curl.dll\n"
                    out.write(line)
        return utils.createShim(os.path.join(self.imageDir(), "dev-utils", "bin", "php.exe"),
                                os.path.join(self.imageDir(), "dev-utils", "php", "php.exe"))
