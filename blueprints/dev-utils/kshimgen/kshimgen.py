import info
from Package.BinaryPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        sums = {"kshimgen-0.2.0-linux-64.tar.xz":"2325dd6b436d70933fde607b538e9fc594552ddc97877017b5a297e69bbde99b",
                "kshimgen-0.2.0-macos-64.tar.xz": "6fe02653ccefe1aac652dde7b9546e8a1a34f9ce912b95ed8cbafbe6c6742f52",
                "kshimgen-0.2.0-windows-32.7z": "e4d25e68bef07c0e31646016a34f6d8bfd0f00568043ac151f44145b4eb4bd4c",
                "kshimgen-0.2.0-windows-64.7z": "9b3f7f03bb3f885184fd9ce16fc83e976e3f44307c6d98e71aca8bb5f399e8db"}
        for ver in ["0.2.0"]:
            fileName = f"kshimgen-{ver}-{CraftCore.compiler.platform.name.lower()}-{CraftCore.compiler.bits}.{'7z' if CraftCore.compiler.isWindows else 'tar.xz'}"
            self.targets[ver] = f"https://files.kde.org/craft/prebuilt/kshimgen/{fileName}"
            self.targetDigests[ver] =  ([sums[fileName]], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '0.2.0'

class Package(BinaryPackageBase):
    def __init__(self, **args):
        BinaryPackageBase.__init__(self)
