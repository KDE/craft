# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.8.4", "1.10.4", "1.11.4", "1.11.8", "1.11.14"]:
            self.targets[ver] = f"http://dbus.freedesktop.org/releases/dbus/dbus-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"dbus-{ver}"
            self.targetConfigurePath[ver] = "cmake"

        self.svnTargets["master"] = "git://anongit.freedesktop.org/git/dbus/dbus"
        self.targetSrcSuffix["master"] = "git"
        self.targetConfigurePath["master"] = "cmake"

        self.patchToApply["1.8.4"] = [("dont_include_afxres.diff", 1)]
        self.patchToApply["1.10.4"] = [("dont_include_afxres.diff", 1)]
        self.patchToApply["1.11.4"] = [("dbus-1.11.4-20160903.diff", 1)]
        self.patchToApply["1.11.14"] = [("dbus-1.11.4-20160903.diff", 1)]

        self.targetDigests["1.10.4"] = "ec1921a09199c81ea20b20448237146a414d51ae"
        self.targetDigests["1.11.4"] = (
            ["474de2afde8087adbd26b3fc5cbf6ec45559763c75b21981169a9a1fbac256c9"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.11.8'] = (
            ['fa207530d694706e33378c87e65b2b4304eb99fff71fc6d6caa6f70591b9afd5'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.11.14'] = (
            ['55cfc7fdd2cccb2fce1f75d2132ad4801b5ed6699fc2ce79ed993574adf90c80'], CraftHash.HashAlgorithm.SHA256)

        self.description = "Freedesktop message bus system (daemon and clients)"
        self.webpage = "http://www.freedesktop.org/wiki/Software/dbus/"
        self.defaultTarget = "1.11.14"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["win32libs/expat"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.package.packageName = "dbus"
        self.subinfo.options.make.slnBaseName = "dbus"
        self.subinfo.options.configure.args = (
            "-DDBUS_BUILD_TESTS=OFF "
            "-DDBUS_ENABLE_XML_DOCS=OFF ")

        if (self.buildType() == "Release"):
            self.subinfo.options.configure.args += (
                "-DDBUS_ENABLE_VERBOSE_MODE=OFF "
                "-DDBUS_DISABLE_ASSERTS=ON ")

        self.subinfo.options.configure.args += (
            "-DDBUS_SESSION_BUS_LISTEN_ADDRESS:STRING=autolaunch:scope=*install-path "
            "-DDBUS_SESSION_BUS_CONNECT_ADDRESS:STRING=autolaunch:scope=*install-path ")
        # kde uses debugger output, so dbus should do too
        self.subinfo.options.configure.args += (
            "-DDBUS_USE_OUTPUT_DEBUG_STRING=ON ")

    def install(self):
        if not CMakePackageBase.install(self): return False

        # TODO: fix
        if self.buildType() == "Debug":
            imagedir = os.path.join(self.installDir(), "lib")
            if craftCompiler.isMSVC():
                if os.path.exists(os.path.join(imagedir, "dbus-1d.lib")):
                    utils.copyFile(os.path.join(imagedir, "dbus-1d.lib"), os.path.join(imagedir, "dbus-1.lib"))
                if not os.path.exists(os.path.join(imagedir, "dbus-1d.lib")):
                    utils.copyFile(os.path.join(imagedir, "dbus-1.lib"), os.path.join(imagedir, "dbus-1d.lib"))
            if craftCompiler.isMinGW():
                if os.path.exists(os.path.join(imagedir, "libdbus-1.dll.a")):
                    utils.copyFile(os.path.join(imagedir, "libdbus-1.dll.a"),
                                   os.path.join(imagedir, "libdbus-1d.dll.a"))

        return True
