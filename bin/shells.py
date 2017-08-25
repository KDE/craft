#!/usr/bin/env python

"""
    provides shells
"""

from CraftCompiler import craftCompiler
from options import *


## \todo requires installed msys package -> add suport for installing packages

class MSysShell(object):
    def __init__(self):
        self.environment = {}

        mergeroot = self.toNativePath(CraftStandardDirs.craftRoot())
        if craftCompiler.isMSVC():
            ldflags = ""
            cflags = " -O2 -MD -GR -W3 -EHsc -D_USE_MATH_DEFINES -DWIN32_LEAN_AND_MEAN -DNOMINMAX -D_CRT_SECURE_NO_WARNINGS"  # dynamic and exceptions enabled
            if craftCompiler.getMsvcPlatformToolset() > 120:
                cflags += " -FS"
        else:
            ldflags = f"-L{mergeroot}/lib "
            cflags = f"-I{mergeroot}/include "

            if self.buildType == "RelWithDebInfo":
                cflags += " -O2 -g "
            elif self.buildType == "Debug":
                cflags += " -O0 -g3 "

        if OsDetection.isWin():
            self.environment["MSYS2_PATH_TYPE"] = "inherit"  # inherit the windows path
            if "make" in self.environment:
                del self.environment["make"]
            if craftCompiler.isMinGW():
                self.environment["MSYSTEM"] = f"MINGW{craftCompiler.bits}_CRAFT"
            elif craftCompiler.isMSVC():
                self.environment["MSYSTEM"] = f"CYGWIN{craftCompiler.bits}_CRAFT"

            if craftCompiler.isMSVC():
                if False:
                    cl = "clang-cl"
                else:
                    cl = "cl"
                self.environment["LIB"] = f"{os.environ['LIB']};{CraftStandardDirs.craftRoot()}\\lib"
                self.environment["INCLUDE"] = f"{os.environ['INCLUDE']};{CraftStandardDirs.craftRoot()}\\include"
                self.environment["LD"] = "link -NOLOGO"
                self.environment["CC"] = "%s -nologo" % cl
                self.environment["CXX"] = self.environment["CC"]
                self.environment["CPP"] = "%s -nologo -EP" % cl
                self.environment["CXXCPP"] = self.environment["CPP"]
                self.environment["NM"] = "dumpbin -symbols"
                self.environment["AR"] = "lib"
                self.environment["WINDRES"] = "rc"
                # self.environment[ "RC","rc-windres"
                self.environment["STRIP"] = ":"
                self.environment["RANLIB"] = ":"
                self.environment["F77"] = "no"
                self.environment["FC"] = "no"

        self.environment["PKG_CONFIG_PATH"] = self.toNativePath(
            os.path.join(CraftStandardDirs.craftRoot(), "lib", "pkgconfig"))


        self.environment["CFLAGS"] = cflags
        self.environment["CXXFLAGS"] = cflags
        self.environment["LDFLAGS"] = ldflags



    @property
    def buildType(self):
        return craftSettings.get("Compile", "BuildType", "RelWithDebInfo")

    @staticmethod
    def toNativePath(path):
        return utils.toMSysPath(path)


    def _findBash(self):
        msysdir = CraftStandardDirs.msysDir()
        bash = utils.utilsCache.findApplication("bash", os.path.join(msysdir, "bin"))
        if not bash:
            bash = utils.utilsCache.findApplication("bash", os.path.join(msysdir, "usr", "bin"))
        if not bash:
            craftDebug.log.critical("Failed to detect bash")
        return bash



    def execute(self, path, cmd, args="", out=sys.stdout, err=sys.stderr, displayProgress=False):

        export = ""
        env = os.environ.copy()
        for k, v in self.environment.items():
            export += "%s='%s' " % (k, v)
            env[k] = v
        command = "%s --login -c \"export %s &&cd %s && %s %s\"" % \
                  (self._findBash(), export, self.toNativePath(path), self.toNativePath(cmd), args)
        craftDebug.step("bash execute: %s" % command)
        craftDebug.log.debug("bash environment: %s" % self.environment)
        return utils.system(command, stdout=out, stderr=err, env=env, displayProgress=displayProgress)

    def login(self):
        self.environment["CHERE_INVOKING"] = "1"
        command = "bash --login -i"
        return self.execute(".", command, displayProgress=True)


def main():
    shell = MSysShell()
    shell.login()


if __name__ == '__main__':
    main()
