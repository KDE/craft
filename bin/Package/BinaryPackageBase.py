#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
import stat
from pathlib import Path

from BuildSystem.BinaryBuildSystem import *
from Package.PackageBase import *
from Packager.TypePackager import TypePackager
from Source.MultiSource import *


class BinaryPackageBase(PackageBase, MultiSource, BinaryBuildSystem, TypePackager):
    """provides a base class for binary packages"""

    def __init__(self, **kwargs):
        CraftCore.log.debug("BinaryPackageBase.__init__ called")
        PackageBase.__init__(self, **kwargs)
        BinaryBuildSystem.__init__(self, **kwargs)
        MultiSource.__init__(self, **kwargs)
        TypePackager.__init__(self, **kwargs)

    def install(self):
        if not BinaryBuildSystem.install(self):
            return False
        if CraftCore.compiler.isMSVC():
            reDlla = re.compile(r"\.dll\.a$")
            reLib = re.compile(r"^lib")
            for f in glob.glob(f"{self.installDir()}/lib/*.dll.a"):
                path, name = os.path.split(f)
                name = re.sub(reDlla, ".lib", name)
                name = re.sub(reLib, "", name)
                dest = Path(path) / name
                if not dest.exists():
                    if not utils.copyFile(f, dest, linkOnly=False):
                        return False
        if CraftCore.compiler.platform.isUnix:
            for f in glob.glob(f"{self.installDir()}/**/*.AppImage", recursive=True):
                appImage = Path(f)
                CraftCore.log.info(f"Make {appImage} executable")
                appImage.chmod(appImage.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        return True
