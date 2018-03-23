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

import info
from Package.MaybeVirtualPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        ver = "2.16.2"
        build = "1"
        self.targets[ver] = f"https://github.com/git-for-windows/git/releases/download/v{ver}.windows.{build}/PortableGit-{ver}-{CraftCore.compiler.bits}-bit.7z.exe"
        self.archiveNames[ver] = f"PortableGit-{ver}-{CraftCore.compiler.bits}-bit.7z"
        self.targetInstallPath[ver] = os.path.join("dev-utils", "git")
        self.targetDigests[ver] = (["b5a91978956ac14f59ccdbc70c9c8d2f105e730e81ae8316a59791d33f3d6a87"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigestsX64[ver] = (['f51853689ad8a9e30759fb263a31bcd59753b3a97272b0e76a4210528a8631a1'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = ver

    def setDependencies(self):
        self.buildDependencies["dev-util/7zip"] = "default"
        self.buildDependencies["gnuwin32/wget"] = "default"
        self.buildDependencies["dev-util/shimgen"] = "default"


from Package.BinaryPackageBase import *


class GitPackage(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def postInstall(self):
        return utils.createShim(os.path.join(self.imageDir(), "dev-utils", "bin", "git.exe"),
                                os.path.join(self.imageDir(), "dev-utils", "git", "bin", "git.exe"))

    def postQmerge(self):
        gitDir = os.path.join(CraftStandardDirs.craftRoot(), self.subinfo.targetInstallPath[self.buildTarget])
        utils.system([os.path.join(gitDir, "git-cmd.exe"), "--no-cd", "--command=post-install.bat"], cwd=gitDir)
        return True


class Package(VirtualIfSufficientVersion):
    def __init__(self):
        VirtualIfSufficientVersion.__init__(self, app="git", version="2.13.0", classA=GitPackage)
