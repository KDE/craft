import shutil

import info
import options
from BuildSystem.BuildSystemBase import *
from utils import ScopedEnv


class PipBuildSystem(BuildSystemBase):
    def __init__(self, package: CraftPackageObject):
        BuildSystemBase.__init__(self, package, "pip")
        self.python2 = False
        self.python3 = True

        self.pipPackageName = self.package.name

    def _getPython2(self):
        if CraftPackageObject.get("dev-utils/python2").isInstalled:
            return "python2"
        python2 = CraftCore.cache.findApplication("python2.7")
        if CraftCore.compiler.isWindows:
            if os.path.exists("C:/python27/python.exe"):
                python2 = "C:/python27/python.exe"
            if not python2 and ("Paths", "PYTHON27") in CraftCore.settings:
                python2 = CraftCore.cache.findApplication("python", CraftCore.settings.get("Paths", "PYTHON27"))
        if not python2:
            CraftCore.log.critical(
                f"Please have a look on {CraftCore.settings.iniPath} and make sure that\n" "\t[Paths]\n" "\tPYTHON27\n" "Points to a valid Python installation."
            )
            return None
        return python2

    def _getPython3(self):
        craftPython = CraftPackageObject.get("libs/python")
        suffix = "_d" if CraftCore.compiler.isWindows and craftPython.instance.subinfo.options.dynamic.buildType == "Debug" else ""
        if CraftPackageObject.get("python-modules/virtualenv").isInstalled:
            if CraftCore.compiler.isWindows:
                return Path(CraftCore.standardDirs.craftRoot()) / f"etc/virtualenv/3/Scripts/python{suffix}"
            else:
                return Path(CraftCore.standardDirs.craftRoot()) / f"etc/virtualenv/3/bin/python3"

        if craftPython.isInstalled:
            python = CraftCore.standardDirs.craftRoot() / f"bin/python{suffix}{CraftCore.compiler.executableSuffix}"
            if python.exists():
                return python
            python = CraftCore.standardDirs.craftRoot() / f"bin/python3{suffix}{CraftCore.compiler.executableSuffix}"
            if python.exists():
                return python
        if not craftPython.categoryInfo.isActive:
            return sys.executable
        raise Exception("Please install libs/python first")

    @property
    def _pythons(self):
        pythons = []
        if self.python2:
            pythons.append(("2", self._getPython2()))
        if self.python3:
            pythons.append(("3", self._getPython3()))
        return pythons

    def venvDir(self, ver):
        return Path(CraftCore.standardDirs.etcDir()) / "virtualenv" / ver

    def make(self):
        if self.subinfo.svnTarget():
            for ver, python in self._pythons:
                if not utils.system([python, "setup.py", "sdist"], cwd=self.sourceDir()):
                    return False
        return True

    def install(self):
        env = {}
        if CraftCore.compiler.isMSVC():
            env.update(
                {
                    "LIB": f"{os.environ['LIB']};{CraftStandardDirs.craftRoot() / 'lib'}",
                    "INCLUDE": f"{os.environ['INCLUDE']};{CraftStandardDirs.craftRoot() / 'include'}",
                }
            )
        with ScopedEnv(env):
            ok = True
            for ver, python in self._pythons:
                command = [
                    python,
                    "-m",
                    "pip",
                    "install",
                    "--upgrade",
                    "--upgrade-strategy",
                    "only-if-needed",
                ]
                if not self.venvDir(ver).exists():
                    command += ["--user"]
                if self.subinfo.svnTarget():
                    command += ["-e", self.sourceDir()]
                elif self.subinfo.hasTarget():
                    command += ["-e", self.sourceDir()]
                else:
                    if self.buildTarget in {"master", "latest"}:
                        command += [self.pipPackageName]
                    else:
                        command += [f"{self.pipPackageName}=={self.buildTarget}"]
                ok = ok and utils.system(command)
            return ok

    def runTest(self):
        return False
