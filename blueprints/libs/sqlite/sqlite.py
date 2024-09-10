# -*- coding: utf-8 -*-
# Copyright 2018 Hannah von Reth <vonreth@kde.org>
# Copyright 2018 Łukasz Wojniłowicz <lukasz.wojnilowicz@gmail.com>
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
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["3.39.2"] = "https://sqlite.org/2022/sqlite-amalgamation-3390200.zip"
        self.targetInstSrc["3.39.2"] = "sqlite-amalgamation-3390200"
        self.targetDigests["3.39.2"] = (["87775784f8b22d0d0f1d7811870d39feaa7896319c7c20b849a4181c5a50609b"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["3.39.2"] = [("sqlite-3.26.0-20181216.diff", 1), ("sqlite-3.31.1-20201026.diff", 1), ("sqlite-3.39.2-20220728.diff", 1)]

        self.targets["3.42.0"] = "https://sqlite.org/2023/sqlite-amalgamation-3420000.zip"
        self.targetInstSrc["3.42.0"] = "sqlite-amalgamation-3420000"
        self.targetDigests["3.42.0"] = (["1cc824d0f5e675829fa37018318fda833ea56f7e9de2b41eddd9f7643b5ec29e"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["3.42.0"] = [(".3.42", 1)]

        self.targets["3.46.0"] = "https://sqlite.org/2024/sqlite-amalgamation-3460000.zip"
        self.targetInstSrc["3.46.0"] = "sqlite-amalgamation-3460000"
        self.targetDigests["3.46.0"] = (["712a7d09d2a22652fb06a49af516e051979a3984adb067da86760e60ed51a7f5"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["3.46.0"] = [(".3.42", 1)]

        self.description = "a library providing a self-contained, serverless, zero-configuration, transactional SQL database engine"
        self.defaultTarget = "3.42.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.subinfo.options.dynamic.buildTools:
            self.subinfo.options.configure.args += ["-DENABLE_SHELL=OFF"]
