# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Hannah von Reth <vonreth@kde.org>

import io
import subprocess

import shells
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
from CraftStandardDirs import CraftStandardDirs
from Package.VirtualPackageBase import VirtualPackageBase
from Utils.Arguments import Arguments


class MsysPackageBase(VirtualPackageBase):
    """provides a base class for packages installed with pacman into msys

    the blueprint needs to depend on dev-utils/msys-base
    by default the package msys/<package name> is installed, set self.msysPackages to override
    """

    def __init__(self, **kwargs):
        CraftCore.log.debug("MsysPackageBase.__init__ called")
        VirtualPackageBase.__init__(self, **kwargs)
        self.msysPackages = [f"msys/{self.package.name}"]

    @staticmethod
    def pacmanOverwriteArgs() -> Arguments:
        useOverwrite = CraftCore.cache.checkCommandOutputFor(CraftStandardDirs.msysDir() / "usr/bin/pacman.exe", "--overwrite", "-Sh")
        # force was replace by overwrite
        return Arguments(["--overwrite='*'" if useOverwrite else "--force"])

    @staticmethod
    def stopMsysProcesses() -> bool:
        return OsUtils.killProcess("*", CraftStandardDirs.msysDir())

    @staticmethod
    def pacmanInstall(packages: list[str]) -> bool:
        shell = shells.BashShell()
        return (
            shell.execute(
                ".",
                "pacman",
                Arguments(["-S"] + packages + ["--noconfirm", MsysPackageBase.pacmanOverwriteArgs(), "--needed"]),
            )
            and MsysPackageBase.stopMsysProcesses()
        )

    def install(self):
        if not super().install():
            return False
        return self.pacmanInstall(self.msysPackages)

    def qmerge(self, dbOnly=True):
        # the files are managed by pacman, never merge or unmerge them
        return super().qmerge(dbOnly=True)

    def sourceRevision(self):
        out = io.BytesIO()
        if not shells.BashShell().execute(".", "pacman", ["-Q"] + [p.split("/")[-1] for p in self.msysPackages], stdout=out, stderr=subprocess.PIPE):
            return ""
        return ", ".join(out.getvalue().decode("UTF-8", errors="replace").strip().splitlines())
