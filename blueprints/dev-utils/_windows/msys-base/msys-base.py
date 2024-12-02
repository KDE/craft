import io
import subprocess
from pathlib import Path

import info
import shells
import utils
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
from CraftStandardDirs import CraftStandardDirs
from Package.BinaryPackageBase import BinaryPackageBase
from Package.MaybeVirtualPackageBase import MaybeVirtualPackageBase
from Package.VirtualPackageBase import VirtualPackageBase
from Utils.Arguments import Arguments


class subinfo(info.infoclass):
    def setTargets(self):
        # as updates are applied with msys and not by craft don't ever change the name of the target, its a bad idea...
        self.targets["base"] = "https://github.com/msys2/msys2-installer/releases/download/2024-11-16/msys2-base-x86_64-20241116.tar.xz"
        self.targetDigestUrls["base"] = f"{self.targets['base']}.sha256"
        self.targetInstSrc["base"] = "msys64"
        self.targetInstallPath["base"] = "msys"

        self.defaultTarget = "base"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

    def updateMsys(self):
        msysDir = CraftCore.settings.get("Paths", "Msys", CraftStandardDirs.craftRoot() / "msys")
        shell = shells.BashShell()
        useOverwrite = CraftCore.cache.checkCommandOutputFor(Path(msysDir) / "usr/bin/pacman.exe", "--overwrite", "-Sh")

        # force was replace by overwrite
        overwrite = Arguments(["--overwrite='*'" if useOverwrite else "--force"])

        def stopProcesses():
            return OsUtils.killProcess("*", msysDir)

        def queryForUpdate():
            out = io.BytesIO()
            if not shell.execute(".", "pacman", Arguments(["-Sy", "--noconfirm", overwrite])):
                raise Exception()
            shell.execute(".", "pacman", ["-Qu", "--noconfirm"], stdout=out, stderr=subprocess.PIPE)
            out = out.getvalue()
            return out != b""

        # start and restart msys before first use
        if not (shell.execute(".", "echo", "Init update", bashArguments=["-l"]) and stopProcesses()):
            return False

        try:
            # max 10 tries
            for _ in range(10):
                if not queryForUpdate():
                    break
                # might return 1 on core updates...
                shell.execute(".", "pacman", Arguments(["-Su", "--noconfirm", overwrite, "--ask", "20"]))
                if not stopProcesses():
                    return False
        except Exception as e:
            CraftCore.log.error(e, exc_info=e)
            return False
        if not (
            shell.execute(
                ".",
                "pacman",
                Arguments(
                    [
                        "-S",
                        "base-devel",
                        "msys/binutils",
                        "msys/autoconf-archive",
                        "msys/autotools",
                        "msys/intltool",
                        "msys/gettext-devel",
                        "--noconfirm",
                        overwrite,
                        "--needed",
                    ]
                ),
            )
            and stopProcesses()
        ):
            return False
        # rebase: Too many DLLs for available address space: Cannot allocate memory => ignore return code ATM
        utils.system("autorebase.bat", cwd=msysDir)
        return True


class MsysPackage(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def postQmerge(self):
        return self.subinfo.updateMsys()


class UpdatePackage(VirtualPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def install(self):
        if not super().install():
            return False
        return self.subinfo.updateMsys()

    def qmerge(self):
        # if it's installed inside of craft we want to update it but never unmerge it
        # if it's an external msys we want to merge the msys.exe helper
        internalMsys = ("Paths", "Msys") not in CraftCore.settings
        return super().qmerge(dbOnly=internalMsys)


class Package(MaybeVirtualPackageBase):
    def __init__(self, **kwargs):
        useExternalMsys = ("Paths", "Msys") in CraftCore.settings
        installMsys = not useExternalMsys and not CraftCore.installdb.isInstalled("dev-utils/msys-base")
        MaybeVirtualPackageBase.__init__(self, **kwargs, condition=installMsys, classA=MsysPackage, classB=UpdatePackage)
        if useExternalMsys:
            # override the install method
            def install():
                CraftCore.log.info(f"Using manually installed msys {CraftStandardDirs.msysDir()}")
                return self.baseClass.install(self)

            setattr(self, "install", install)
