import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.10.3", "2.12.7", "2.14.4", "2.14.5"]:
            self.targets[ver] = f"https://download.gnome.org/sources/libxml2/{'.'.join(ver.split('.')[:-1])}/libxml2-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"libxml2-{ver}"
        self.targetDigests["2.10.3"] = (["5d2cc3d78bec3dbe212a9d7fa629ada25a7da928af432c93060ff5c17ee28a9c"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.12.7"] = (["24ae78ff1363a973e6d8beba941a7945da2ac056e19b53956aeb6927fd6cfb56"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.14.4"] = (["24175ec30a97cfa86bdf9befb7ccf4613f8f4b2713c5103e0dd0bc9c711a2773"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.14.5"] = (["03d006f3537616833c16c53addcdc32a0eb20e55443cba4038307e3fa7d8d44b"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["2.10.3"] = [
            ("libxml2-2.10.3-20221105.diff", 1),
            ("libxml2-2.10.3-20221114.diff", 1),
            ("libxml2-android-ecm-toolchain-workaround.diff", 1),
        ]
        self.patchLevel["2.10.3"] = 3

        self.patchToApply["2.14.4"] = [(".2.14.4", 1)]
        self.patchLevel["2.14.4"] = 1

        # This patch partly reverts https://gitlab.gnome.org/GNOME/libxml2/-/commit/c106455c2571c20a0c66942db29247490ac626e9
        # because it introduced "Cflags.private: -DLIBXML_STATIC" to libxml-2.0.pc
        # which leads to a link error in shared-mime-info on MSVC
        # This should be reported upstream, but it is not clear to me
        # if this is a libxml2 or shared-mime-info bug
        self.patchToApply["2.14.5"] = [("msvc-no-forced-static.diff", 1)]

        self.svnTargets["master"] = "https://gitlab.gnome.org/GNOME/libxml2.git"

        self.description = "XML C parser and toolkit (runtime and applications)"
        self.defaultTarget = "2.14.5"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/liblzma"] = None
        self.runtimeDependencies["libs/iconv"] = None
        self.runtimeDependencies["libs/icu"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            "-DLIBXML2_WITH_PYTHON=OFF",
            f"-DLIBXML2_WITH_ICU={self.subinfo.options.isActive('libs/icu').asOnOff}",
            f"-DLIBXML2_WITH_LZMA={self.subinfo.options.isActive('libs/liblzma').asOnOff}",
            # we use the system iconv on macOS
            f"-DLIBXML2_WITH_ICONV={(self.subinfo.options.isActive('libs/iconv') or CraftCore.compiler.isMacOS).asOnOff}",
        ]
        if CraftCore.compiler.isAndroid:
            self.subinfo.options.configure.args += ["-DLIBXML2_WITH_PROGRAMS=OFF", "-DLIBXML2_WITH_TESTS=OFF"]
