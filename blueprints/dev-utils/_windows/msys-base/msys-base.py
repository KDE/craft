import io
import subprocess

import info
import shells
import utils
from CraftCore import CraftCore
from CraftStandardDirs import CraftStandardDirs
from Package.BinaryPackageBase import BinaryPackageBase
from Package.MaybeVirtualPackageBase import MaybeVirtualPackageBase
from Package.MsysPackageBase import MsysPackageBase
from Package.VirtualPackageBase import VirtualPackageBase
from Utils.Arguments import Arguments


class subinfo(info.infoclass):
    def setTargets(self):
        # as updates are applied with msys and not by craft don't ever change the name of the target, its a bad idea...
        self.targets["base"] = "https://github.com/msys2/msys2-installer/releases/download/2026-09-27/msys2-base-x86_64-20260927.tar.xz"
        self.targetDigestUrls["base"] = f"{self.targets['base']}.sha256"
        self.targetInstSrc["base"] = "msys64"
        self.targetInstallPath["base"] = "msys"

        self.defaultTarget = "base"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

    def updateMsys(self):
        msysDir = CraftStandardDirs.msysDir()
        shell = shells.BashShell()
        stopProcesses = MsysPackageBase.stopMsysProcesses

        def queryForUpdate():
            out = io.BytesIO()
            if not shell.execute(".", "pacman", ["-Sy", "--noconfirm"]):
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
                shell.execute(".", "pacman", Arguments(["-Su", "--noconfirm", "--overwrite='*'", "--ask", "20"]))
                if not stopProcesses():
                    return False
        except Exception as e:
            CraftCore.log.error(e, exc_info=e)
            return False
        if not MsysPackageBase.pacmanInstall(["base-devel", "msys/binutils", "msys/autoconf-archive", "msys/intltool", "msys/gettext-devel"]):
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
