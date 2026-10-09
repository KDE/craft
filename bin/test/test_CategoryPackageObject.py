import tempfile
from pathlib import Path

import CraftTestBase
from Blueprints.CraftPackageObject import CategoryPackageObject, CraftPackageObject
from CraftCompiler import CraftCompiler, CraftCompilerSignature
from CraftCore import CraftCore


class TestCategoryPackageObjectIsActive(CraftTestBase.CraftTestBase):
    def setUp(self):
        super().setUp()
        self._oldSignature = CraftCore.compiler.signature
        self.blueprintDir = tempfile.TemporaryDirectory()
        self.blueprintRoot = Path(self.blueprintDir.name) / "blueprints"
        self.blueprintRoot.mkdir()

    def tearDown(self):
        CraftCore.compiler.signature = self._oldSignature
        self.blueprintDir.cleanup()
        super().tearDown()

    def _setTarget(self, abi: str, host: str = None):
        hostSignature = CraftCompilerSignature.parseAbi(host, None) if host else None
        CraftCore.compiler.signature = CraftCompilerSignature.parseAbi(abi, hostSignature)

    def _category(self, path: str, **general) -> CategoryPackageObject:
        localPath = self.blueprintRoot / path
        localPath.mkdir(parents=True, exist_ok=True)
        if general:
            with (localPath / "info.ini").open("wt") as ini:
                ini.write("[General]\n")
                for k, v in general.items():
                    ini.write(f"{k} = {v}\n")
        return CategoryPackageObject(self.blueprintRoot, localPath)

    def test_noInfoIni(self):
        self._setTarget("linux-gcc-x86_64")
        category = self._category("libs")
        self.assertFalse(category.valid)
        self.assertTrue(category.isActive)

    def test_defaults(self):
        self._setTarget("windows-cl-msvc2022-x86_64")
        category = self._category("libs", description="foo")
        self.assertTrue(category.valid)
        self.assertTrue(category.isActive)

    def test_platforms(self):
        self._setTarget("linux-gcc-x86_64")
        self.assertTrue(self._category("linux", platforms="Linux").isActive)
        self.assertTrue(self._category("unix", platforms="Unix").isActive)
        self.assertTrue(self._category("multi", platforms="Windows;Linux").isActive)
        self.assertFalse(self._category("windows", platforms="Windows").isActive)
        self.assertFalse(self._category("apple", platforms="Apple").isActive)
        self.assertTrue(self._category("unixNotAndroid", platforms="Unix;~Android").isActive)

    def test_platformsInverted(self):
        self._setTarget("windows-cl-msvc2022-x86_64")
        self.assertFalse(self._category("notWindows", platforms="~Windows").isActive)
        self.assertTrue(self._category("notLinux", platforms="~Linux").isActive)
        self.assertFalse(self._category("notWindowsLinux", platforms="~Windows;Linux").isActive)

    def test_compiler(self):
        self._setTarget("windows-cl-msvc2022-x86_64")
        self.assertTrue(self._category("cl", compiler="CL").isActive)
        self.assertFalse(self._category("gcc", compiler="GCC").isActive)
        self.assertFalse(self._category("gccLike", compiler="GCCLike").isActive)
        self.assertFalse(self._category("notCl", compiler="~CL").isActive)

        self._setTarget("linux-clang-x86_64")
        self.assertTrue(self._category("clangGccLike", compiler="GCCLike").isActive)
        self.assertFalse(self._category("clangCl", compiler="CL").isActive)

    def test_architecture(self):
        self._setTarget("macos-clang-arm64")
        self.assertTrue(self._category("arm64", architecture="arm64").isActive)
        self.assertFalse(self._category("x86_64", architecture="x86_64").isActive)
        self.assertFalse(self._category("notArm64", architecture="~arm64").isActive)

    def test_combined(self):
        self._setTarget("windows-cl-msvc2022-arm64")
        self.assertTrue(self._category("match", platforms="Windows", compiler="CL", architecture="arm64").isActive)
        self.assertFalse(self._category("wrongArch", platforms="Windows", compiler="CL", architecture="x86_64").isActive)
        self.assertFalse(self._category("wrongCompiler", platforms="Windows", compiler="GCC", architecture="arm64").isActive)
        self.assertFalse(self._category("wrongPlatform", platforms="Linux", compiler="CL", architecture="arm64").isActive)

    def test_crossCompile(self):
        self._setTarget("android-clang-arm64", host="linux-gcc-x86_64")
        self.assertTrue(self._category("android", platforms="Android").isActive)
        self.assertTrue(self._category("mobile", platforms="Mobile").isActive)
        self.assertFalse(self._category("linux", platforms="Linux").isActive)
        self.assertTrue(self._category("arm64", architecture="arm64").isActive)
        self.assertFalse(self._category("x86_64", architecture="x86_64").isActive)
        # no restrictions must not exclude cross compiling
        self.assertTrue(self._category("defaults", description="foo").isActive)
        self.assertFalse(self._category("native", platforms="Native").isActive)
        self.assertTrue(self._category("notNative", platforms="~Native").isActive)
        self.assertFalse(self._category("archNative", architecture="Native").isActive)
        self.assertTrue(self._category("unixNotAndroid", platforms="Unix").isActive)
        self.assertFalse(self._category("unixNotAndroid2", platforms="Unix;~Android").isActive)

    def test_inheritedFromParent(self):
        self._setTarget("linux-gcc-x86_64")
        self._category("windows-only", platforms="Windows")
        child = self._category("windows-only/child")
        self.assertTrue(child.valid)
        self.assertFalse(child.isActive)

        self._setTarget("windows-cl-msvc2022-x86_64")
        self.assertTrue(child.isActive)

    def test_native(self):
        self._setTarget("linux-gcc-x86_64")
        self.assertTrue(self._category("native", platforms="Native").isActive)
        self.assertFalse(self._category("notNative", platforms="~Native").isActive)
        self.assertTrue(self._category("linuxNative", platforms="Linux;Native").isActive)
        self.assertFalse(self._category("windowsNative", platforms="Windows;Native").isActive)
        self.assertTrue(self._category("archNative", architecture="Native").isActive)

        # same platform, different architecture
        self._setTarget("linux-gcc-arm64", host="linux-gcc-x86_64")
        self.assertTrue(self._category("platformNative", platforms="Linux;Native").isActive)
        self.assertFalse(self._category("archNative", architecture="Native").isActive)
        self.assertTrue(self._category("archNotNative", architecture="~Native").isActive)

    def test_architectureModifiers(self):
        self._setTarget("linux-gcc-x86_64")
        self.assertTrue(self._category("bits64", architecture="bits64").isActive)
        self.assertFalse(self._category("bits32", architecture="bits32").isActive)
        self.assertTrue(self._category("mixed", architecture="x86_64;arm32").isActive)
        self.assertFalse(self._category("x86_32", architecture="x86_32").isActive)
        self.assertFalse(self._category("not64", architecture="~bits64").isActive)

        self._setTarget("linux-gcc-arm32", host="linux-gcc-x86_64")
        self.assertTrue(self._category("mixed", architecture="x86_64;arm32").isActive)
        self.assertFalse(self._category("x86_32", architecture="x86_32").isActive)
        self.assertFalse(self._category("bits64", architecture="bits64").isActive)

        self._setTarget("linux-gcc-arm64", host="linux-gcc-x86_64")
        self.assertFalse(self._category("mixed", architecture="x86_64;arm32").isActive)

    def test_mingw(self):
        self._setTarget("windows-gcc-x86_64")
        self.assertTrue(self._category("gcc", compiler="GCC").isActive)
        self.assertTrue(self._category("mingw", compiler="MinGW").isActive)
        self.assertFalse(self._category("gccNoMinGW", compiler="GCC;~MinGW").isActive)
        self.assertFalse(self._category("cl", compiler="CL").isActive)

        self._setTarget("linux-gcc-x86_64")
        self.assertFalse(self._category("mingw", compiler="MinGW").isActive)
        self.assertTrue(self._category("gccNoMinGW", compiler="GCC;~MinGW").isActive)

    def test_nativeOnlyBlueprint(self):
        self._setTarget("linux-gcc-x86_64")
        self.assertTrue(CraftPackageObject.get("libs/python").instance.package.categoryInfo.isActive)
        self._setTarget("android-clang-arm64", host="linux-gcc-x86_64")
        self.assertFalse(CraftPackageObject.get("libs/python").instance.package.categoryInfo.isActive)

    def test_blueprintOperators(self):
        Platforms = CraftCore.compiler.Platforms
        Compiler = CraftCore.compiler.Compiler
        self._setTarget("android-clang-arm64", host="linux-gcc-x86_64")

        category = self._category("notAndroid")
        category.platforms = ~Platforms.Android
        self.assertFalse(category.isActive)
        category.platforms = ~~Platforms.Android
        self.assertTrue(category.isActive)

        category = self._category("native")
        category.platforms &= Platforms.Native
        self.assertFalse(category.isActive)
        category = self._category("notNative")
        category.platforms &= ~Platforms.Native
        self.assertTrue(category.isActive)

        category = self._category("restricted", platforms="Unix")
        category.platforms &= ~Platforms.Android
        self.assertFalse(category.isActive)
        category.platforms |= Platforms.Mobile
        self.assertTrue(category.isActive)

        category = self._category("noCompiler")
        category.compiler = Compiler.NoCompiler
        self.assertFalse(category.isActive)
        category.compiler = Compiler.GCCLike
        self.assertTrue(category.isActive)

        self._setTarget("windows-gcc-x86_64")
        category = self._category("mingwOnly")
        category.compiler &= Compiler.MinGW
        self.assertTrue(category.isActive)
        self._setTarget("windows-cl-msvc2022-x86_64")
        self.assertFalse(category.isActive)

    def test_excludeMinGW(self):
        notMinGW = self._category("notMinGW")
        notMinGW.compiler &= ~CraftCompiler.Compiler.MinGW
        # the original flags are preserved
        gccLikeNotMinGW = self._category("gccLikeNotMinGW", compiler="GCCLike")
        gccLikeNotMinGW.compiler &= ~CraftCompiler.Compiler.MinGW

        self._setTarget("windows-gcc-x86_64")
        self.assertFalse(notMinGW.isActive)
        self.assertFalse(gccLikeNotMinGW.isActive)

        self._setTarget("windows-cl-msvc2022-x86_64")
        self.assertTrue(notMinGW.isActive)
        self.assertFalse(gccLikeNotMinGW.isActive)

        self._setTarget("windows-clang-x86_64")
        self.assertTrue(notMinGW.isActive)
        self.assertTrue(gccLikeNotMinGW.isActive)

        self._setTarget("linux-gcc-x86_64")
        self.assertTrue(notMinGW.isActive)
        self.assertTrue(gccLikeNotMinGW.isActive)

    def test_architectureHelpers(self):
        Architecture = CraftCore.compiler.Architecture
        self.assertTrue(Architecture.x86_64.isX86_64)
        self.assertFalse(Architecture.arm64.isX86_64)
        self.assertFalse(Architecture.x86_32.isArm32)
        self.assertTrue(Architecture.arm64.isArm64)
        self.assertTrue(Architecture.arm64e.isArm64)
        self.assertTrue(Architecture.arm64e.isArm64e)
        self.assertFalse(Architecture.arm64.isArm64e)
