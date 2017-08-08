import shutil

import info
from Package.BinaryPackageBase import *


# currently only needed from kdenetwork


class subinfo(info.infoclass):
    def setTargets(self):
        baseURL = "http://dev.mysql.com/get/Downloads/MySQL-5.7/"
        ver = '5.7.18'
        arch = "32"
        if craftCompiler.isX64():
            arch = "x64"
        self.targets[ver] = f"{baseURL}mysql-{ver}-win{arch}.zip"
        self.targetInstSrc[ver] = f"mysql-{ver}-win{arch}"

        self.description = "MySql database server and embedded library"
        self.defaultTarget = ver

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.package.disableStriping = True
        self.subinfo.options.package.packSources = False

    def install(self):
        shutil.copytree(os.path.join(self.sourceDir(), "bin"), os.path.join(self.installDir(), "bin"),
                        ignore=shutil.ignore_patterns('*.pdb', '*.map', '*test*', 'mysqld-debug.exe', '*.pl', 'debug*'))
        shutil.copy(os.path.join(self.sourceDir(), "lib", "libmysqld.dll"),
                    os.path.join(self.installDir(), "bin", "libmysqld.dll"))
        shutil.copy(os.path.join(self.sourceDir(), "lib", "libmysql.dll"),
                    os.path.join(self.installDir(), "bin", "libmysql.dll"))
        shutil.copytree(os.path.join(self.sourceDir(), "lib"), os.path.join(self.installDir(), "lib"),
                        ignore=shutil.ignore_patterns('*.pdb', '*.map', 'debug*', 'libmysqld.dll', 'libmysql.dll',
                                                      'mysql*'))
        if craftCompiler.isMinGW():
            utils.createImportLibs("libmysqld", self.installDir())
            utils.createImportLibs("libmysql", self.installDir())
        shutil.copytree(os.path.join(self.sourceDir(), "include"), os.path.join(self.installDir(), "include"),
                        ignore=shutil.ignore_patterns('*.def'))
        shutil.copytree(os.path.join(self.sourceDir(), "share"), os.path.join(self.installDir(), "share"),
                        ignore=shutil.ignore_patterns('Makefile*'))
        return True

    def qmerge(self):
        if not BinaryPackageBase.qmerge(self):
            return False
        return self.system("mysqld --console --initialize-insecure")
