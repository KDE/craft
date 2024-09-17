import multiprocessing
import os
from pathlib import Path

import info
import utils
from BuildSystem.BuildSystemBase import BuildSystemBase
from CraftCompiler import CraftCompiler
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.MakeFilePackageBase import MakeFilePackageBase
from Utils import CraftHash
from Utils.Arguments import Arguments


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms &= CraftCore.compiler.Platforms.Native

    def setTargets(self):
        for ver in ["5.36.0", "5.38.2", "5.39.8", "5.40.1"]:
            self.targets[ver] = f"https://www.cpan.org/src/5.0/perl-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"perl-{ver}"

        if CraftCore.compiler.platform.isWindows:
            self.patchToApply["5.36.0"] = [(".perl-5.36.0_win", 1)]
        else:
            self.patchToApply["5.36.0"] = [(".perl-5.36.0", 1)]

        if CraftCore.compiler.platform.isWindows:
            self.patchToApply["5.38.2"] = [(".perl-5.39.8_win", 1)]
            self.patchToApply["5.39.8"] = [(".perl-5.39.8_win", 1)]
            self.patchToApply["5.40.1"] = [(".perl-5.39.8_win", 1)]
        else:
            self.patchToApply["5.38.2"] = [(".perl-5.36.0", 1)]
            self.patchToApply["5.39.8"] = [(".perl-5.36.0", 1)]
            self.patchToApply["5.40.1"] = [(".perl-5.36.0", 1)]
        self.targetDigests["5.36.0"] = (["e26085af8ac396f62add8a533c3a0ea8c8497d836f0689347ac5abd7b7a4e00a"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["5.38.2"] = (["a0a31534451eb7b83c7d6594a497543a54d488bc90ca00f5e34762577f40655e"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["5.39.8"] = (["25f8b4db7a7d91c051b1c2594ed83c291c74c1012da559a8d580755b598bb7e3"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["5.40.1"] = (["02f8c45bb379ed0c3de7514fad48c714fd46be8f0b536bfd5320050165a1ee26"], CraftHash.HashAlgorithm.SHA256)
        self.description = (
            "Perl 5 is a highly capable, feature-rich programming language with over 30 years of "
            "development. Perl 5 runs on over 100 platforms from portables to mainframes and is "
            "suitable for both rapid prototyping and large scale development projects."
        )
        self.patchLevel["5.38.2"] = 4
        self.defaultTarget = "5.40.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class PackageMSVC(MakeFilePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.make.supportsMultijob = False
        self.subinfo.options.useShadowBuild = False

        root = OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())
        config = {
            "CCTYPE": "MSVC141" if CraftCore.compiler.compiler.isMSVC else "GCC",
            "CRAFT_DESTDIR": self.installDir(),
            "CRAFT_WIN64": "" if CraftCore.compiler.architecture.isX86_64 else "undef",
            "PLMAKE": "nmake" if CraftCore.compiler.compiler.isMSVC else "mingw32-make",
        }

        if CraftCore.compiler.compiler.isMinGW:
            config["CCHOME"] = os.path.join(CraftCore.standardDirs.craftRoot(), "mingw64")
            config["SHELL"] = os.environ["COMSPEC"]
            config["CRAFT_CFLAGS"] = f"{os.environ.get('CFLAGS', '')} -I'{root}/include' -L'{root}/lib' -Wno-error=implicit-function-declaration"
            config["USE_MINGW_ANSI_STDIO"] = "define"
            config["USE_64_BIT_INT"] = "define"
            config["CCTYPE"] = "GCC"
            self.subinfo.options.make.args += [f"-j{CraftCore.settings.get('Compile', 'Jobs', multiprocessing.cpu_count())}"]
        elif CraftCore.compiler.architecture.isX86_32:
            config["PROCESSOR_ARCHITECTURE"] = f"x{CraftCore.compiler.architecture.bits}"

        self.subinfo.options.make.args += ["{0}={1}".format(x, y) for x, y in config.items()]
        self.subinfo.options.install.args += self.subinfo.options.make.args + ["installbare"]

    def _globEnv(self):
        env = {}
        if CraftCore.compiler.compiler.isMSVC:
            env = {"PATH": f"{self.blueprintDir()};{os.environ['PATH']}"}
        return env

    def make(self):
        with utils.ScopedEnv(self._globEnv()):
            os.chdir(self.sourceDir() / "win32")
            return utils.system(Arguments([self.makeProgram, self.makeOptions(self.subinfo.options.make.args)]))

    def install(self):
        with utils.ScopedEnv(self._globEnv()):
            if not BuildSystemBase.install(self):
                return False

            os.chdir(self.sourceDir() / "win32")
            if not utils.system(Arguments([self.makeProgram, self.makeOptions(self.subinfo.options.install.args), f"DESTDIR={self.installDir()}"])):
                return False

        def makeWriatable(root):
            with os.scandir(root) as scan:
                for f in scan:
                    utils.makeWritable(f.path)
                    if f.is_dir():
                        makeWriatable(f.path)

        makeWriatable(self.installDir())
        return True

    def postInstall(self):
        # in difference to the defaultePrefix replace, we replace the installDir with the installPrefix
        # not an older install prefix with another
        newPrefix = OsUtils.toUnixPath(self.installPrefix())
        oldPrefixes = [self.installDir()]
        files = utils.filterDirectoryContent(
            self.installDir(), whitelist=lambda x, root: Path(x).suffix in BuildSystemBase.PatchableFile, blacklist=lambda x, root: True
        )
        return self.patchInstallPrefix(files, oldPrefixes, newPrefix)


class PackageAutoTools(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # https://metacpan.org/pod/distribution/perl/INSTALL
        self.subinfo.options.install.args = Arguments(["install.perl"])
        self.subinfo.options.configure.args = Arguments(
            [
                "-des",
                "-D",
                f"prefix={self.installPrefix()}",
                "-D",
                "mksymlinks",
                "-D",
                "userelocatableinc",
                "-U",
                "default_inc_excludes_dot",
                "-D",
                "usethreads",
            ]
        )

        cflags = self.shell.environment["CFLAGS"]
        ldflags = self.shell.environment["LDFLAGS"]
        if CraftCore.compiler.compiler.isGCC and not CraftCore.compiler.architecture.isNative and CraftCore.compiler.architecture.isX86_32:
            cflags += " -m32"
            ldflags += " -m32"
            self.subinfo.options.configure.args += ["-Alddlflags=-m32 -shared", "-Uuse64bitint -Uuse64bitall"]
        if CraftCore.compiler.platform.isMacOS and not CraftCore.compiler.architecture.isNative:
            cflags = f"-arch {CraftCore.compiler.architecture.name.lower()} {cflags}"
            ldflags = f"-arch {CraftCore.compiler.architecture.name.lower()} {ldflags}"
            self.subinfo.options.configure.args += [
                f"-Dcc={os.environ['CC']} -arch {CraftCore.compiler.architecture.name.lower()}",
                f"-Dcxx={os.environ['CXX']} -arch {CraftCore.compiler.architecture.name.lower()}",
                f"-Dld={os.environ['CC']} -arch {CraftCore.compiler.architecture.name.lower()}",
            ]
        if CraftCore.compiler.platform.isMacOS:
            lddflags = "-dylib"
        else:
            lddflags = "-shared"
        self.subinfo.options.configure.args += [
            f"-Accflags={cflags}",
            f"-Aldflags={ldflags}",
        ]

    def configure(self):
        self.enterBuildDir()
        return self.shell.execute(self.buildDir(), self.sourceDir() / "Configure", self.subinfo.options.configure.args)

    def install(self):
        if not super().install():
            return False

        def makeWriatable(root):
            with os.scandir(root) as scan:
                for f in scan:
                    utils.makeWritable(f.path)
                    if f.is_dir():
                        makeWriatable(f.path)

        makeWriatable(self.installDir())
        return True

    def postInstall(self):
        hardCoded = [os.path.join(self.imageDir(), x) for x in ["bin/pod2man"]]
        return self.patchInstallPrefix(hardCoded, self.subinfo.buildPrefix, CraftCore.standardDirs.craftRoot())

    @property
    def makeProgram(self):
        if CraftCore.compiler.platform.isFreeBSD:
            return "make"
        else:
            return super().makeProgram


if CraftCore.compiler.platform.isUnix:

    class Package(PackageAutoTools):
        pass

else:

    class Package(PackageMSVC):
        pass
