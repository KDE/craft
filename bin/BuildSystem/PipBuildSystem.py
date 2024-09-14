import os
import sys
from pathlib import Path

import utils
from Blueprints.CraftPackageObject import CraftPackageObject
from BuildSystem.BuildSystemBase import BuildSystemBase
from CraftCore import CraftCore
from CraftStandardDirs import CraftStandardDirs
from utils import ScopedEnv


class PipBuildSystem(BuildSystemBase):
    def __init__(self, package: CraftPackageObject):
        BuildSystemBase.__init__(self, package, "pip")
        self.python3 = True
        self.usesCraftPython = CraftPackageObject.get("libs/python").categoryInfo.isActive

        self.pipPackageName = self.package.name
        self.usePipBinaryPackages = True

    def _getPython3(self):
        craftPython = CraftPackageObject.get("libs/python")
        suffix = "_d" if CraftCore.compiler.platform.isWindows and craftPython.instance.subinfo.options.dynamic.buildType == "Debug" else ""
        if CraftPackageObject.get("python-modules/virtualenv").isInstalled:
            if CraftCore.compiler.platform.isWindows:
                return self.venvDir("3") / f"Scripts/python{suffix}"
            else:
                return self.venvDir("3") / "bin/python3"

        if craftPython.isInstalled:
            python = CraftCore.standardDirs.craftRoot() / f"bin/python{suffix}{CraftCore.compiler.platform.executableSuffix}"
            if python.exists():
                return python
            python = CraftCore.standardDirs.craftRoot() / f"bin/python3{suffix}{CraftCore.compiler.platform.executableSuffix}"
            if python.exists():
                return python
        if not self.usesCraftPython:
            return sys.executable
        raise Exception("Please install libs/python first")

    @property
    def _pythons(self):
        pythons = []
        if self.python3:
            pythons.append(("3", self._getPython3()))
        print(pythons)
        return pythons

    def venvDir(self, ver) -> Path:
        return Path(CraftCore.standardDirs.etcDir()) / "virtualenv" / ver

    def make(self):
        if self.subinfo.svnTarget():
            for ver, python in self._pythons:
                if not utils.system([python, "setup.py", "sdist"], cwd=self.sourceDir()):
                    return False
        return True

    def install(self):
        env = {}
        if CraftCore.compiler.compiler.isMSVC:
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
                if not self.usePipBinaryPackages:
                    command += ["--no-binary", ":all:", "--no-cache-dir"]
                if self.usesCraftPython:
                    command += ["--prefix", self.installDir()]
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

