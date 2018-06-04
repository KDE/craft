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

from BuildSystem.BuildSystemBase import *


class MSBuildBuildSystem(BuildSystemBase):
    def __init__(self):
        BuildSystemBase.__init__(self, "msbuild")
        self.msbuildTargets = ["Rebuild"]
        self.buildTypes = {"Release" : "Release", "RelWithDebInfo" : "Release", "Debug" : "Debug" }

    def configure(self, defines=""):
        return True

    def make(self):
        self.enterSourceDir()
        buildType =self.buildTypes[self.buildType()]
        if CraftCore.compiler.isX86():
            platform = " /p:Platform=win32"
        else:
            platform = ""
        if "WINDOWSSDKVERSION" in os.environ:
            sdkVer = " /p:WindowsTargetPlatformVersion={0}".format(os.environ["WINDOWSSDKVERSION"].replace("\\", ""))
        else:
            sdkVer = ""
        for target in self.msbuildTargets:
            if not utils.system(f"msbuild /m /t:{target} \"{self.subinfo.options.configure.projectFile}\""
                                f" /p:Configuration={buildType}"
                                f" /tv:{CraftCore.compiler.getInternalVersion()}.0"
                                f" /p:PlatformToolset=v{CraftCore.compiler.getMsvcPlatformToolset()}"
                                f"{sdkVer}"
                                f"{platform}"
                                f" {self.subinfo.options.configure.args}"):
                return False
        return True

    def install(self, buildDirs=None, installHeaders=True):
        if not buildDirs:
            buildDirs = [self.sourceDir()]

        self.cleanImage()

        for dir in ["bin", "lib", "include"]:
            if not os.path.exists(os.path.join(self.installDir(), dir)):
                os.makedirs(os.path.join(self.installDir(), dir))


        def globCopy(sourceDir : str, destDir : str, patterns : [str]):
            for pattern in patterns:
                for f in glob.glob(os.path.join(sourceDir, pattern), recursive=True):
                    if not utils.copyFile(f, os.path.join(destDir, os.path.basename(f)), linkOnly=False):
                        return False
            return True

        for root in buildDirs:
            if not globCopy(root, os.path.join(self.imageDir(), "lib"), ["**/*.pdb", "**/*.lib"]):
                return False
            if not globCopy(root, os.path.join(self.imageDir(), "bin"), ["**/*.pdb", "**/*.exe", "**/*.dll"]):
                return False
            if installHeaders:
                if not globCopy(root, os.path.join(self.imageDir(), "include"), ["**/*.h", "**/*.hpp"]):
                    return False
        return True

    def unittest(self):
        return True
