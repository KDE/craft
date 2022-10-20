import configparser

import CraftTestBase
from CraftCompiler import CraftCompiler, CraftCompilerSignature


class TestCompilerSeignature(CraftTestBase.CraftTestBase):
    def test(self):
        self.assertEqual(
            CraftCompilerSignature.parseAbi("windows-msvc2019_64-cl").signature,
            CraftCompilerSignature(CraftCompiler.Platforms.Windows, CraftCompiler.Compiler.CL, "msvc2019", CraftCompiler.Architecture.x86_64).signature,
        )
        self.assertEqual(
            CraftCompilerSignature.parseAbi("windows-msvc2019-cl-x86_64").signature,
            CraftCompilerSignature(CraftCompiler.Platforms.Windows, CraftCompiler.Compiler.CL, "msvc2019", CraftCompiler.Architecture.x86_64).signature,
        )
        self.assertEqual(
            CraftCompilerSignature.parseAbi("windows-gcc-x86_64").signature,
            CraftCompilerSignature(CraftCompiler.Platforms.Windows, CraftCompiler.Compiler.GCC, None, CraftCompiler.Architecture.x86_64).signature,
        )
        self.assertEqual(
            CraftCompilerSignature.parseAbi("macos-clang-arm64").signature,
            CraftCompilerSignature(CraftCompiler.Platforms.MacOS, CraftCompiler.Compiler.CLANG, None, CraftCompiler.Architecture.arm64).signature,
        )
        self.assertEqual(
            CraftCompilerSignature.parseAbi("android-arm64-clang").signature,
            CraftCompilerSignature(CraftCompiler.Platforms.Android, CraftCompiler.Compiler.CLANG, "arm64-v8a", CraftCompiler.Architecture.arm64).signature,
        )
        self.assertEqual(
            CraftCompilerSignature.parseAbi("android-clang-arm").signature,
            CraftCompilerSignature(CraftCompiler.Platforms.Android, CraftCompiler.Compiler.CLANG, "armeabi-v7a", CraftCompiler.Architecture.arm).signature,
        )
        self.assertEqual(
            CraftCompilerSignature.parseAbi("android-clang-arm64").signature,
            CraftCompilerSignature(CraftCompiler.Platforms.Android, CraftCompiler.Compiler.CLANG, "arm64-v8a", CraftCompiler.Architecture.arm64).signature,
        )
        self.assertEqual(
            CraftCompilerSignature.parseAbi("linux-64-gcc").signature,
            CraftCompilerSignature(CraftCompiler.Platforms.Linux, CraftCompiler.Compiler.GCC, None, CraftCompiler.Architecture.x86_64).signature,
        )
        self.assertEqual(
            CraftCompilerSignature.parseAbi("linux-gcc-x86_64").signature,
            CraftCompilerSignature(CraftCompiler.Platforms.Linux, CraftCompiler.Compiler.GCC, None, CraftCompiler.Architecture.x86_64).signature,
        )
