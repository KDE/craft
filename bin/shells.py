#!/usr/bin/env python

"""
    provides shells
"""

from CraftStandardDirs import CraftStandardDirs
from CraftOS.OsDetection import OsDetection
from options import *
import tempfile


class BashShell(object):
    def __init__(self):
        self._environment = {}
        self._useMSVCCompatEnv = False


    @property
    def useMSVCCompatEnv(self):
        return self._useMSVCCompatEnv

    @useMSVCCompatEnv.setter
    def useMSVCCompatEnv(self, b):
        self._useMSVCCompatEnv = b
        self._environment = {}

    @property
    def environment(self):
        if not self._environment:

            mergeroot = self.toNativePath(CraftStandardDirs.craftRoot())
            cflags = ""
            ldflags = ""
            if not CraftCore.compiler.isMSVC():
                ldflags = f"-L{mergeroot}/lib "
                cflags = f"-I{mergeroot}/include "

                if self.buildType == "RelWithDebInfo":
                    cflags += " -O2 -g "
                elif self.buildType == "Debug":
                    cflags += " -O0 -g3 "

            if OsDetection.isWin():
                path = "/usr/local/bin:/usr/bin:/bin:/usr/bin/site_perl:/usr/bin/vendor_perl:/usr/bin/core_perl"
                if CraftCore.compiler.isMinGW():
                    gcc = shutil.which("gcc")
                    if gcc:
                        path = f"{self.toNativePath(os.path.dirname(gcc))}:{path}"
                for p in os.environ["PATH"].split(";"):
                    path += f":{self.toNativePath(p)}"
                self._environment["PATH"] = path
                if "make" in self._environment:
                    del self._environment["make"]
                if CraftCore.compiler.isMinGW():
                    self._environment["MSYSTEM"] = f"MINGW{CraftCore.compiler.bits}_CRAFT"
                elif CraftCore.compiler.isMSVC():
                    self._environment["MSYSTEM"] = f"CYGWIN{CraftCore.compiler.bits}_CRAFT"

                if self.useMSVCCompatEnv and CraftCore.compiler.isMSVC():
                    self._environment["LIB"] = f"{os.environ['LIB']};{CraftStandardDirs.craftRoot()}\\lib"
                    self._environment["INCLUDE"] = f"{os.environ['INCLUDE']};{CraftStandardDirs.craftRoot()}\\include"

                    if False:
                        cl = "clang-cl"
                    else:
                        cl = "cl"
                    self._environment["LD"] = "link -NOLOGO"
                    self._environment["CC"] = f"{cl} -nologo"
                    self._environment["CXX"] = self._environment["CC"]
                    self._environment["CPP"] = f"{cl} -nologo -EP"
                    self._environment["CXXCPP"] = self._environment["CPP"]
                    self._environment["NM"] = "dumpbin -symbols"
                    self._environment["AR"] = "lib"
                    self._environment["WINDRES"] = "rc"
                    # self.environment[ "RC","rc-windres"
                    self._environment["STRIP"] = ":"
                    self._environment["RANLIB"] = ":"
                    self._environment["F77"] = "no"
                    self._environment["FC"] = "no"

                    ldflags = ""
                    cflags = " -O2 -MD -GR -W3 -EHsc -D_USE_MATH_DEFINES -DWIN32_LEAN_AND_MEAN -DNOMINMAX -D_CRT_SECURE_NO_WARNINGS"  # dynamic and exceptions enabled
                    if CraftCore.compiler.getMsvcPlatformToolset() > 120:
                        cflags += " -FS"

            self._environment["PKG_CONFIG_PATH"] = self.toNativePath(
                os.path.join(CraftStandardDirs.craftRoot(), "lib", "pkgconfig"))


            self._environment["CFLAGS"] = cflags
            self._environment["CXXFLAGS"] = cflags
            self._environment["LDFLAGS"] = ldflags
        return self._environment

    @property
    def buildType(self):
        return CraftCore.settings.get("Compile", "BuildType", "RelWithDebInfo")

    @staticmethod
    def toNativePath(path):
        if OsUtils.isWin():
            return OsUtils.toMSysPath(path)
        else:
            return path

    def _findBash(self):
        msysdir = CraftStandardDirs.msysDir()
        bash = CraftCore.cache.findApplication("bash", os.path.join(msysdir, "bin"))
        if not bash:
            bash = CraftCore.cache.findApplication("bash", os.path.join(msysdir, "usr", "bin"))
        if not bash:
            CraftCore.log.critical("Failed to detect bash")
        return bash

    def execute(self, path, cmd, args="", out=sys.stdout, err=sys.stderr, displayProgress=False, envDir=None):
        tmpDir = None
        if not envDir:
            tmpDir = tempfile.TemporaryDirectory()
            envDir = tmpDir.name

        export = []
        for k, v in self.environment.items():
            export.append(f"export {k}='{v}'\n")
        if CraftCore.debug.verbose() >= 1:
            # log msys env
            export.append("printenv\n")
            CraftCore.log.debug(export)

        envPath = os.path.join(envDir, f"craft_environment_{os.path.basename(cmd)}.sh")
        with open(envPath, "wt+") as env:
            env.writelines(export)
        msysEnv = self.toNativePath(envPath)
        command = f"{self._findBash()} --login -c \"source {msysEnv} && cd {self.toNativePath(path)} && {self.toNativePath(cmd)} {args}\""
        CraftCore.debug.step("bash execute: %s" % command)
        CraftCore.log.debug("bash environment: %s" % self.environment)

        out = utils.system(command, stdout=out, stderr=err, displayProgress=displayProgress)
        if tmpDir:
            tmpDir.cleanup()
        return out

    def login(self):
        if CraftCore.compiler.isMSVC():
            self.useMSVCCompatEnv = True
        self.environment["CHERE_INVOKING"] = "1"
        self.environment["MSYS2_PATH_TYPE"] = "inherit"
        return self.execute(".", "bash",  "--norc --login -i", displayProgress=True)

def main():
    shell = BashShell()
    shell.login()

if __name__ == '__main__':
    main()
