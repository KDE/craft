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


from BuildSystem.BuildSystemBase import *


class MesonBuildSystem(BuildSystemBase):
    
    def __init__(self):
        BuildSystemBase.__init__(self, "meson")

    def __env(self):
            env = {
                "LDFLAGS" : self.subinfo.options.configure.ldflags + " " + os.environ.get("LDFLAGS", ""),
                "CFLAGS" : self.subinfo.options.configure.cflags + " " + os.environ.get("CFLAGS", "")
            }
            if CraftCore.compiler.isMSVC():
                env.update({
                    "LIB" : f"{os.environ['LIB']};{os.path.join(CraftStandardDirs.craftRoot() , 'lib')}",
                    "INCLUDE" : f"{os.environ['INCLUDE']};{os.path.join(CraftStandardDirs.craftRoot() , 'include')}"
                    })
            else:
                env["LDFLAGS"] = f"-L{CraftStandardDirs.craftRoot() / 'lib'} {env['LDFLAGS']}"
                env["CFLAGS"] = f"-I{CraftStandardDirs.craftRoot() / 'include'} {env['CFLAGS']}"
            return env

    
    def configureOptions(self, defines=""):
        buildType = {"Release": "release", "RelWithDebInfo": "debugoptimized", "Debug" : "debug"}.get(self.buildType())
        return Arguments([defines,
                             "--prefix", CraftCore.standardDirs.craftRoot(),
                             "--libdir", "lib",
                             "--datadir", CraftCore.standardDirs.locations.data,
                             "--buildtype", buildType,
                             "--cmake-prefix-path", CraftCore.standardDirs.craftRoot(),
                             self.buildDir(),
                             "-Ddefault_library=shared",
                             BuildSystemBase.configureOptions(self)
        ])

    def configure(self, defines=""):
        with utils.ScopedEnv(self.__env()):
            return utils.system(Arguments(["meson", self.configureOptions(defines)]), cwd=self.sourceDir())

    def make(self):
        with utils.ScopedEnv(self.__env()):
            return utils.system(Arguments(["meson", "compile", self.makeOptions(self.subinfo.options.make.args)]), cwd=self.buildDir())

    def install(self):
        """install the target"""
        if not BuildSystemBase.install(self):
            return False
        env = self.__env()
        env["DESTDIR"] = self.installDir()
        with utils.ScopedEnv(env):
            return utils.system(["meson", "install"], cwd=self.buildDir()) and self._fixInstallPrefix()

    def unittest(self):
        """running make tests"""
        return utils.system(["meson", "test"], cwd=self.buildDir())
