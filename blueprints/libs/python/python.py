# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Hannah von Reth <vonreth@kde.org>

import glob
import sys
from pathlib import Path

import info
import utils
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.MSBuildPackageBase import MSBuildPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotAndroid
        if CraftCore.compiler.isMinGW():
            self.parent.package.categoryInfo.compiler = CraftCore.compiler.Compiler.NoCompiler

    def setTargets(self):
        for ver in ["3.11.5", "3.11.7"]:
            self.targets[ver] = f"https://www.python.org/ftp/python/{ver}/Python-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"Python-{ver}"
        self.targetDigests["3.11.5"] = (["85cd12e9cf1d6d5a45f17f7afe1cebe7ee628d3282281c492e86adf636defa3f"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["3.11.7"] = (["18e1aa7e66ff3a58423d59ed22815a6954e53342122c45df20c96877c062b9b7"], CraftHash.HashAlgorithm.SHA256)
        if CraftCore.compiler.isMSVC():
            self.patchToApply["3.11.5"] = [(".msvc/patches", 1)]
            self.patchToApply["3.11.7"] = [(".msvc/patches", 1)]

        self.patchLevel["3.11.5"] = 4
        self.patchLevel["3.11.7"] = 1

        self.description = "Python is a high-level, general-purpose programming language"
        self.defaultTarget = "3.11.7"

    def setDependencies(self):
        self.buildDependencies["dev-utils/automake"] = None
        self.runtimeDependencies["libs/libbzip2"] = None
        self.runtimeDependencies["libs/expat"] = None
        self.runtimeDependencies["libs/openssl"] = None
        self.runtimeDependencies["libs/gettext"] = None
        self.runtimeDependencies["libs/sqlite"] = None
        self.runtimeDependencies["libs/libffi"] = None
        self.runtimeDependencies["libs/liblzma"] = None


if CraftCore.compiler.isMSVC():

    class Package(MSBuildPackageBase):
        def __init__(self, **args):
            super().__init__()
            # msvc support and patches are based on https://github.com/microsoft/vcpkg/tree/0e47c1985273129e4d0ee52ff73bed9125555de8/ports/python3
            self.subinfo.options.configure.projectFile = self.sourceDir() / "PCbuild/pcbuild.proj"
            self.subinfo.options.configure.args += [
                "/p:IncludeExtensions=true",
                "/p:IncludeExternals=true",
                "/p:IncludeCTypes=true",
                "/p:IncludeSSL=true",
                "/p:IncludeTkinter=false",
                "/p:IncludeTests=false",
                f"/p:ForceImportBeforeCppTargets={self.sourceDir()}/PCbuild/python_vcpkg.props",
            ]

        def configure(self, defines=""):
            vars = {"VCPKG_LIBRARY_LINKAGE": "dynamic", "CURRENT_INSTALLED_DIR": CraftCore.standardDirs.craftRoot(), "VCPKG_TARGET_ARCHITECTURE": "x64"}

            def addLib(key, libName, libNameDebug=None):
                if not libNameDebug:
                    libNameDebug = libName
                vars[f"{key}_RELEASE"] = CraftCore.standardDirs.craftRoot() / f"lib/{libName}.lib"
                vars[f"{key}_DEBUG"] = CraftCore.standardDirs.craftRoot() / f"lib/{libNameDebug}.lib"

            addLib("BZ2", "bzip2", "bzip2d")
            addLib("CRYPTO", "libcrypto")
            addLib("EXPAT", "libexpat")
            addLib("FFI", "libffi")
            addLib("LZMA", "liblzma")
            addLib("SQLITE", "sqlite3")
            addLib("SSL", "libssl")
            addLib("ZLIB", "zlib")
            if not utils.configureFile(self.blueprintDir() / ".msvc/python_vcpkg.props.in", self.sourceDir() / "PCbuild/python_vcpkg.props", vars):
                return False
            if not utils.configureFile(self.blueprintDir() / ".msvc/openssl.props.in", self.sourceDir() / "PCbuild/openssl.props", vars):
                return False

            with (self.sourceDir() / "PCbuild/libffi.props").open("wt", encoding="UTF-8") as out:
                out.write("<?xml version='1.0' encoding='utf-8'?><Project xmlns='http://schemas.microsoft.com/developer/msbuild/2003' />")

            return super().configure()

        def make(self):
            with utils.ScopedEnv({"PythonForBuild": sys.executable}):
                return super().make()

        def install(self):
            self.cleanImage()
            verMinor = self.subinfo.buildTarget.split(".")[1]
            debugSuffix = "_d" if self.buildType() == "Debug" else ""
            for p in ["python", "pythonw", "venvlauncher", "venvwlauncher"]:
                if not utils.copyFile(self.sourceDir() / f"PCbuild/amd64/{p}{debugSuffix}.exe", self.imageDir() / f"bin/{p}{debugSuffix}.exe"):
                    return False
                if self.buildType() == "Debug":
                    if not utils.createShim(self.imageDir() / f"bin/{p}.exe", self.imageDir() / f"bin/{p}{debugSuffix}.exe"):
                        return False
            if not self._globCopy(self.sourceDir() / "PCbuild/amd64/", self.imageDir() / "bin", ["*.dll"]):
                return False
            for p in ["python3", f"python3{verMinor}"]:
                if not utils.copyFile(self.sourceDir() / f"PCbuild/amd64/{p}{debugSuffix}.lib", self.imageDir() / f"lib/{p}.lib"):
                    return False
            if not self._globCopy(self.sourceDir() / "PCbuild/amd64/", self.imageDir() / f"bin/DLLs", ["*.pyd"]):
                return False
            if not utils.copyDir(self.sourceDir() / "Include/", self.imageDir() / f"include/python3.{verMinor}"):
                return False
            if not utils.copyFile(self.sourceDir() / "PC/pyconfig.h", self.imageDir() / f"include/python3.{verMinor}/pyconfig.h"):
                return False
            if not utils.copyDir(self.sourceDir() / "Lib", self.imageDir() / "bin/Lib"):
                return False
            return True

else:

    class Package(AutoToolsPackageBase):
        def __init__(self, **args):
            super().__init__()
            self.shell.useMSVCCompatEnv = True
            # we call it specially in configure
            self.subinfo.options.configure.autoreconf = False
            self.subinfo.options.configure.args += [
                "--without-static-libpython",
                "--enable-ipv6",
                "--with-system-expat",
                "--with-pkg-config=yes",
                "--enable-loadable-sqlite-extensions",
                "--with-libc=",
                # if enabled it will somtimes install pip sometimes not,
                # if needed we can still call python3 -m ensurepip
                "--with-ensurepip=no",
            ]
            if CraftCore.compiler.isMacOS:
                self.subinfo.options.configure.noLibDir = True
                self.subinfo.options.configure.args += [f"--enable-framework={CraftCore.standardDirs.craftRoot()}/lib"]
                self.subinfo.options.install.args += [f"PYTHONAPPSDIR={CraftCore.standardDirs.craftRoot()}"]
            else:
                self.subinfo.options.configure.args += [
                    "--enable-shared",
                ]

        def install(self):
            self.subinfo.options.make.supportsMultijob = False
            if not super().install():
                return False
            if CraftCore.compiler.isMacOS:
                minorVersion = self.buildTarget.split(".")[1]
                if not utils.system(
                    ["install_name_tool", "-id", f"@rpath/Python.framework/Versions/3.{minorVersion}/Python", self.imageDir() / "lib/Python.framework/Python"]
                ):
                    return False
                # python needs argv0 to be the location of the binary
                # this doesn't work with symlinks, therefor we use shims
                binDir = self.imageDir() / "bin"
                for x in binDir.iterdir():
                    if x.is_symlink():
                        # the link points to the installation prefix...
                        dest = Path(x.readlink()).relative_to(CraftCore.standardDirs.craftRoot())
                        x.unlink()
                        # now we are located in bin, but dest is relative to the root
                        if not utils.createShim(x, Path("..") / dest):
                            return False

                pkgconfigDir = self.imageDir() / "lib/Python.framework/Versions/Current/lib/pkgconfig/"
                pkgconfigDirDest = self.imageDir() / "lib/pkgconfig"
                pkgconfigDirDest.mkdir(exist_ok=True, parents=True)
                for x in pkgconfigDir.glob("*.pc"):
                    if not utils.createSymlink(x, pkgconfigDirDest / x.name):
                        return False
            return True

        def unittest(self):
            # https://github.com/Homebrew/homebrew-core/blob/6cf9a08bcd4afc6633d45ec31aba27e7b3beda78/Formula/p/python@3.11.rb#L496
            for module in ["sqlite3", "_ctypes", "_decimal", "pyexpat", "readline", "zlib"]:
                if not utils.system([self.imageDir() / "bin/python3", "-c", f"import {module}"]):
                    return False
            return True
