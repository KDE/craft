import os
import sys
from pathlib import Path

import utils
from Blueprints.CraftPackageObject import CraftPackageObject
from BuildSystem.BuildSystemBase import BuildSystemBase
from CraftCore import CraftCore
from utils import ScopedEnv
from Utils.Arguments import Arguments


class PipBuildSystem(BuildSystemBase):
    def __init__(self, package: CraftPackageObject):
        BuildSystemBase.__init__(self, package, "pip")
        self._python = None
        self.allowNotVenv = False
        self.allowPrebuildBinaries = False
        self.pipPackageName = self.package.name
        self._isPipTarget = not (self.subinfo.hasTarget() or self.subinfo.svnTarget())

    @property
    def python(self):
        if not self._python:
            craftPython = CraftPackageObject.get("libs/python")
            if not craftPython.categoryInfo.isActive:
                if CraftCore.compiler.platform.isWindows:
                    pythonExe = self.venvDir() / f"Scripts/python{CraftCore.compiler.platform.executableSuffix}"
                else:
                    pythonExe = self.venvDir() / "bin/python3"
                if pythonExe.exists():
                    self._python = pythonExe
                else:
                    # don't cache the system python location
                    return sys.executable
            elif craftPython.isInstalled:
                suffix = "_d" if CraftCore.compiler.platform.isWindows and craftPython.instance.subinfo.options.dynamic.buildType == "Debug" else ""
                python = CraftCore.standardDirs.craftRoot() / f"bin/python{suffix}{CraftCore.compiler.platform.executableSuffix}"
                if python.exists():
                    self._python = python
                else:
                    python = CraftCore.standardDirs.craftRoot() / f"bin/python3{suffix}{CraftCore.compiler.platform.executableSuffix}"
                    if python.exists():
                        self._python = python
            if not self._python:
                raise Exception("Please install libs/python first")
        return self._python

    def venvDir(self):
        return Path(CraftCore.standardDirs.etcDir()) / "virtualenv/3"

    def createMacOSPipShims(self, binaries: list[str]):
        if not CraftCore.compiler.platform.isMacOS:
            return True

        for binary in binaries:
            if not utils.createShim(
                self.installDir() / f"bin/{binary}{CraftCore.compiler.platform.executableSuffix}",
                self.installDir() / f"lib/Python.framework/Versions/Current/bin/{binary}{CraftCore.compiler.platform.executableSuffix}",
                useAbsolutePath=False,
            ):
                return False
        return True

    def make(self):
        if self._isPipTarget:
            return True

        setupFile = self.sourceDir() / "setup.py"
        # See https://bernat.tech/posts/pep-517-518/
        if setupFile.is_file():
            # This is the legacy approach
            if not utils.system([self.python, "setup.py", "sdist", "--dist-dir", self.buildDir()], cwd=self.sourceDir()):
                return False
        else:
            # The modern approach
            if not utils.system([self.python, "-m", "build", "--outdir", self.buildDir()], cwd=self.sourceDir()):
                return False
        return True

    def install(self):
        env = {}
        bootstrap = False
        if CraftCore.compiler.compiler.isMSVC:
            tmpDir = CraftCore.standardDirs.junctionsDir() / "tmp"
            tmpDir.mkdir(parents=True, exist_ok=True)
            env.update(
                {
                    # we can't use a normal short path as python would resolve it
                    "TMPDIR": tmpDir,
                }
            )
        if self.supportsCCACHE:
            cxx = CraftCore.standardDirs.craftRoot() / "dev-utils/ccache/bin" / Path(os.environ["CXX"]).name
            if CraftCore.compiler.platform.isWindows and not cxx.suffix:
                cxx = Path(str(cxx) + CraftCore.compiler.platform.executableSuffix)
            if cxx.exists():
                env["CXX"] = cxx
                env["CC"] = cxx.parent / Path(os.environ["CC"]).name

        with ScopedEnv(env):
            usesCraftPython = CraftPackageObject.get("libs/python").categoryInfo.isActive

            command = Arguments([self.python])
            if self.pipPackageName in ["pip", "pip-system"]:
                bootstrap = True
                command += [self.localFilePath()[0]]
            else:
                bootstrap = False
                command += ["-m", "pip"]
            command += ["install", "--upgrade", "--no-input", "--verbose"]
            command += self.subinfo.options.configure.args

            if usesCraftPython:
                # we can only cache stuff if we actually do something
                command += [
                    "--force-reinstall",
                ]
                if self._isPipTarget and not self.allowPrebuildBinaries:
                    # Build binaries ourself when installing from pip.
                    # In case we use a SVN or tarball target we don't want
                    # to enforce that here, because already done via the make step
                    command += [
                        "--no-binary",
                        ":all:",
                        "--no-cache-dir",
                        "--no-build-isolation",
                        "--config-settings=--global-option=build_ext",
                        f"--config-settings=--global-option=--include-dirs={CraftCore.standardDirs.craftRoot()}/include",
                        f"--config-settings=--global-option=--library-dirs={CraftCore.standardDirs.craftRoot()}/lib",
                    ]
                command += ["--root", self.installDir()]
            elif not self.allowNotVenv:
                command += ["--require-virtualenv"]

            if not self._isPipTarget and not bootstrap:
                # Installing with wildcards (pip install dir/*) does not work on Windows,
                # hence we use the --find-links approach which might be a bit cleaner anyway.
                # See https://stackoverflow.com/questions/48183160/how-to-pip-install-whl-on-windows-using-a-wildcard
                command += ["--no-index", "--find-links", self.buildDir(), self.pipPackageName]
            else:
                if self.buildTarget in {"master", "latest"}:
                    command += [self.pipPackageName]
                else:
                    command += [f"{self.pipPackageName}=={self.buildTarget}"]
            if not utils.system(command):
                return False
            if usesCraftPython:
                if not self._fixInstallPrefix():
                    return False
            return True

    def runTest(self):
        return False

    def createPackage(self):
        if self.subinfo.options.isActive("libs/python"):
            return super().createPackage()
        return True
