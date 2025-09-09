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

import glob
import os
import re

import utils
from Blueprints.CraftPackageObject import CraftPackageObject
from BuildSystem.BuildSystemBase import BuildSystemBase
from CraftCore import CraftCore
from CraftStandardDirs import CraftStandardDirs


class MSBuildBuildSystem(BuildSystemBase):
    def __init__(self, package: CraftPackageObject):
        BuildSystemBase.__init__(self, package, "msbuild")
        self.msbuildTargets = ["Rebuild"]
        self.buildTypes = {
            "Release": "Release",
            "RelWithDebInfo": "Release",
            "MinSizeRel": "Release",
            "Debug": "Debug",
        }

    def _globCopy(self, sourceDir: str, destDir: str, patterns: list[str]):
        for pattern in patterns:
            for f in glob.glob(os.path.join(sourceDir, pattern), recursive=True):
                if not utils.copyFile(f, os.path.join(destDir, os.path.basename(f)), linkOnly=False):
                    return False
        return True

    def configure(self, defines=""):
        return True

    def make(self):
        env = {
            "LIB": f"{os.environ['LIB']};{os.path.join(CraftStandardDirs.craftRoot() , 'lib')}",
            "INCLUDE": f"{os.environ['INCLUDE']};{os.path.join(CraftStandardDirs.craftRoot() , 'include')}",
        }
        with utils.ScopedEnv(env):
            self.enterSourceDir()
            msbuildVersion = CraftCore.cache.getVersion("msbuild", versionCommand="-ver", pattern=re.compile(r"(\d+\.\d+)"))
            buildType = self.buildTypes[self.buildType()]
            if CraftCore.compiler.architecture.isX86_32:
                platform = " /p:Platform=win32"
            else:
                platform = ""
            if "WINDOWSSDKVERSION" in os.environ:
                sdkVer = " /p:WindowsTargetPlatformVersion={0}".format(os.environ["WINDOWSSDKVERSION"].replace("\\", ""))
            else:
                sdkVer = ""
            toolsVersion = f"{CraftCore.compiler.getInternalVersion()}.0"
            if toolsVersion == "15.0" and msbuildVersion >= "16":
                toolsVersion = " /toolsversion:Current"
            elif os.path.exists(r"C:\Program Files (x86)\MSBuild\{0}".format(toolsVersion)):
                toolsVersion = f" /toolsversion:{toolsVersion}"
            else:
                toolsVersion = ""
            return utils.system(
                f"msbuild /m /t:{';'.join(self.msbuildTargets)} \"{self.subinfo.options.configure.projectFile}\""
                f" /p:Configuration={buildType}"
                f" /p:PlatformToolset=v{CraftCore.compiler.getMsvcPlatformToolset()}"
                f"{toolsVersion}"
                f"{sdkVer}"
                f"{platform}"
                f" {self.subinfo.options.configure.args}"
            )

    def install(self, buildDirs=None, installHeaders=True):
        if not buildDirs:
            buildDirs = [self.sourceDir()]

        self.cleanImage()

        for dir in ["bin", "lib", "include"]:
            if not os.path.exists(os.path.join(self.installDir(), dir)):
                os.makedirs(os.path.join(self.installDir(), dir))

        for root in buildDirs:
            if not self._globCopy(root, os.path.join(self.imageDir(), "lib"), ["**/*.lib"]):
                return False
            if not self._globCopy(root, os.path.join(self.imageDir(), "bin"), ["**/*.exe", "**/*.dll"]):
                return False
            if installHeaders:
                if not self._globCopy(
                    root,
                    os.path.join(self.imageDir(), "include"),
                    ["**/*.h", "**/*.hpp"],
                ):
                    return False
        return True

    def unittest(self):
        return True
