# -*- coding: utf-8 -*-
# Copyright Hannah von Reth <vonreth@kde.org>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

import os
from pathlib import Path

import info
import utils
from CraftCore import CraftCore
from CraftStandardDirs import CraftStandardDirs
from Package.BinaryPackageBase import BinaryPackageBase
from Package.MaybeVirtualPackageBase import VirtualIfSufficientVersion
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        ver = "2.49.0"
        build = "1"
        self.targets[ver] = f"https://github.com/git-for-windows/git/releases/download/v{ver}.windows.{build}/PortableGit-{ver}-64-bit.7z.exe"
        self.archiveNames[ver] = f"PortableGit-{ver}-64-bit.7z"
        self.targetInstallPath[ver] = os.path.join("dev-utils", "git")
        self.targetDigests[ver] = (
            ["bc980a64e875304ea5aa88386fda37e8a0089d0f2023616b9995b1ca75b471dd"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.defaultTarget = ver

    def setDependencies(self):
        self.buildDependencies["dev-utils/7zip"] = None
        self.buildDependencies["dev-utils/wget"] = None
        self.buildDependencies["dev-utils/kshimgen"] = None

    def locateGit(self) -> Path:
        gitPath = CraftCore.cache.findApplication("git")
        if not gitPath:
            return None
        # check whether git is installed by the system or us
        if (CraftCore.standardDirs.craftRoot() / "dev-utils") in gitPath.parents:
            return CraftCore.standardDirs.craftRoot() / "dev-utils/git/bin"
        return gitPath.parent


class GitPackage(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def postInstall(self):
        env = None
        if CraftCore.compiler.platform.isWindows:
            env = {"TERM": ""}
        return utils.createShim(
            self.imageDir() / "dev-utils/bin/git.exe",
            self.imageDir() / "dev-utils/git/bin/git.exe",
            env=env,
        )

    def postQmerge(self):
        gitDir = CraftStandardDirs.craftRoot() / self.subinfo.targetInstallPath[self.buildTarget]
        utils.system(
            [
                gitDir / "git-cmd.exe",
                "--no-cd",
                "--command=post-install.bat",
            ],
            cwd=gitDir,
        )
        return True


class Package(VirtualIfSufficientVersion):
    def __init__(self, **kwargs):
        VirtualIfSufficientVersion.__init__(self, **kwargs, app="git", version="2.27.0", classA=GitPackage)
