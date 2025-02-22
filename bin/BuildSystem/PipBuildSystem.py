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

        self.subinfo.options.package.disableBinaryCache = True
        self.allowNotVenv = False
        self.allowPrebuildBinaries = False

        self._isPipTarget = not (self.subinfo.hasTarget() or self.subinfo.svnTarget())

    def _getPython3(self):
        craftPython = CraftPackageObject.get("libs/python")
        suffix = "_d" if CraftCore.compiler.isWindows and craftPython.instance.subinfo.options.dynamic.buildType == "Debug" else ""
        if CraftPackageObject.get("python-modules/virtualenv").isInstalled:
            if CraftCore.compiler.isWindows:
                return self.venvDir("3") / f"Scripts/python{suffix}"
            else:
                return self.venvDir("3") / "bin/python3"

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
        if self.python3:
            pythons.append(("3", self._getPython3()))
        return pythons

    def venvDir(self, ver):
        return Path(CraftCore.standardDirs.etcDir()) / "virtualenv" / ver

    def createMacOSPipShims(self, binaries: list[str]):
        if not CraftCore.compiler.isMacOS:
            return True

        for binary in binaries:
            if not utils.createShim(
                self.installDir() / f"bin/{binary}{CraftCore.compiler.executableSuffix}",
                self.installDir() / f"lib/Python.framework/Versions/Current/bin/{binary}{CraftCore.compiler.executableSuffix}",
                useAbsolutePath=True,
            ):
                return False
        return True

    def make(self):
        if self._isPipTarget:
            return True

        setupFile = self.sourceDir() / "setup.py"
        for ver, python in self._pythons:
            # See https://bernat.tech/posts/pep-517-518/
            if setupFile.is_file():
                # This is the legacy approach
                if not utils.system([python, "setup.py", "sdist", "--dist-dir", self.buildDir()], cwd=self.sourceDir()):
                    return False
            else:
                # The modern approach
                if not utils.system([python, "-m", "build", "--outdir", self.buildDir()], cwd=self.sourceDir()):
                    return False

        return True

    def install(self):
        env = {}
        if CraftCore.compiler.isMSVC():
            tmpDir = CraftCore.standardDirs.junctionsDir() / "tmp"
            tmpDir.mkdir(parents=True, exist_ok=True)
            env.update(
                {
                    "LIB": f"{os.environ['LIB']};{CraftStandardDirs.craftRoot() / 'lib'}",
                    "INCLUDE": f"{os.environ['INCLUDE']};{CraftStandardDirs.craftRoot() / 'include'}",
                    # we can't use a normal short path as python would resolve it
                    "TMPDIR": tmpDir,
                }
            )
        if self.supportsCCACHE:
            cxx = CraftCore.standardDirs.craftRoot() / "dev-utils/ccache/bin" / Path(os.environ["CXX"]).name
            if CraftCore.compiler.isWindows and not cxx.suffix:
                cxx = Path(str(cxx) + CraftCore.compiler.executableSuffix)
            if cxx.exists():
                env["CXX"] = cxx
                env["CC"] = cxx.parent / Path(os.environ["CC"]).name
        with ScopedEnv(env):
            ok = True
            for ver, python in self._pythons:
                command = [python, "-m", "pip", "install", "--upgrade", "--no-input", "--verbose"]

                usesCraftPython = CraftPackageObject.get("libs/python").categoryInfo.isActive
                if usesCraftPython:
                    if self._isPipTarget and not self.allowPrebuildBinaries:
                        # Build binaries ourself when installing from pip.
                        # In case we use a SVN or tarball target we don't want
                        # to enforce that here, because already done via the make step
                        command += ["--no-binary", ":all:", "--no-cache-dir"]

                    if CraftCore.compiler.isMacOS:
                        # On macOS we use a frameworks
                        # While on Linux modules are installed to PREFIX/lib/site-packages on macOS a versioned path
                        # like PREFIX/lib/python3.11/site-packages would be used if set prefix outsite the framwork
                        prefix = self.installDir() / "lib/Python.framework/Versions/Current"
                    else:
                        prefix = self.installDir()
                    command += ["--prefix", prefix]
                elif not self.allowNotVenv:
                    command += ["--require-virtualenv"]

                if not self._isPipTarget:
                    # Installing with wildcards (pip install dir/*) does not work on Windows,
                    # hence we use the --find-links approach which might be a bit cleaner anyway.
                    # See https://stackoverflow.com/questions/48183160/how-to-pip-install-whl-on-windows-using-a-wildcard
                    command += ["--no-index", "--find-links", self.buildDir(), self.pipPackageName]
                else:
                    if self.buildTarget in {"master", "latest"}:
                        command += [self.pipPackageName]
                    else:
                        command += [f"{self.pipPackageName}=={self.buildTarget}"]
                ok = ok and utils.system(command)
            return ok

    def runTest(self):
        return False
