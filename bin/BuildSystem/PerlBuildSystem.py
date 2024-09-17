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

import utils
from BuildSystem.MakeFileBuildSystem import MakeFileBuildSystem
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
from Utils.Arguments import Arguments


# based on https://wiki.archlinux.org/index.php/Perl_package_guidelines
class PerlBuildSystem(MakeFileBuildSystem):
    def __init__(self, **kwargs):
        MakeFileBuildSystem.__init__(self, **kwargs)
        self.subinfo.options.make.supportsMultijob = False
        self.subinfo.options.useShadowBuild = False

    def configure(self):
        self.enterBuildDir()
        env = {
            "PERL5LIB": None,
            "PERL_MM_OPT": None,
            "PERL_LOCAL_LIB_ROOT": None,
            "PERL_MM_USE_DEFAULT": "1",
            "PERL_AUTOINSTALL": "--skipdeps",
        }
        with utils.ScopedEnv(env):
            return utils.system(Arguments.formatCommand(["perl", "Makefile.PL"], self.subinfo.options.configure.args))

    def make(self):
        self.enterBuildDir()
        env = {
            "PERL5LIB": None,
            "PERL_MM_OPT": None,
            "PERL_LOCAL_LIB_ROOT": None,
            "PERL_MM_USE_DEFAULT": "1",
            "PERL_AUTOINSTALL": "--skipdeps",
        }
        if CraftCore.compiler.compiler.isMSVC:
            root = OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())
            env.update(
                {
                    "INCLUDE": f"{os.environ['INCLUDE']};{root}/include",
                    "LIB": f"{os.environ['LIB']};{root}/lib",
                }
            )
        with utils.ScopedEnv(env):
            return utils.system([self.makeProgram])

    def install(self):
        env = {"PERL5LIB": None, "PERL_MM_OPT": None, "PERL_LOCAL_LIB_ROOT": None}
        with utils.ScopedEnv(env):
            if 1 and CraftCore.compiler.platform.isWindows:
                # ugly hack to make destdir work, it probably breaks some scripts
                makeFile = self.buildDir() / "Makefile"
                with open(makeFile, "rt") as make:
                    txt = make.read()
                with open(makeFile, "wt") as make:
                    txt = txt.replace(
                        str(CraftCore.standardDirs.craftRoot()),
                        str(CraftCore.standardDirs.craftRoot())[2:],
                    )
                    make.write(txt)
            if not (super().install() and self._fixInstallPrefix()):
                return False

            def makeWriatable(root):
                with os.scandir(root) as scan:
                    for f in scan:
                        utils.makeWritable(f.path)
                        if f.is_dir():
                            makeWriatable(f.path)

            makeWriatable(self.installDir())
            return True
