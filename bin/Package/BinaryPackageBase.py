#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
from BuildSystem.BinaryBuildSystem import *
from Package.PackageBase import *
from Packager.TypePackager import *
from Source.MultiSource import *

from pathlib import Path
import stat

class BinaryPackageBase(PackageBase, MultiSource, BinaryBuildSystem, TypePackager):
    """provides a base class for binary packages"""

    def __init__(self):
        CraftCore.log.debug("BinaryPackageBase.__init__ called")
        PackageBase.__init__(self)
        BinaryBuildSystem.__init__(self)
        MultiSource.__init__(self)
        TypePackager.__init__(self)

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
        if CraftCore.compiler.isUnix:
            for f in glob.glob(f"{self.installDir()}/**/*.AppImage", recursive=True):
                appImage = Path(f)
                CraftCore.log.info(f"Make {appImage} executable")
                appImage.chmod(appImage.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        return True
