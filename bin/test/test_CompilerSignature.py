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
            CraftCompilerSignature.parseAbi("macos-clang-arm64").signature,
            CraftCompilerSignature(CraftCompiler.Platforms.MacOS, CraftCompiler.Compiler.CLANG, None, CraftCompiler.Architecture.arm64).signature,
        )
        self.assertEqual(
            CraftCompilerSignature.parseAbi("android-arm64-clang").signature,
            CraftCompilerSignature(CraftCompiler.Platforms.Android, CraftCompiler.Compiler.CLANG, "arm64-v8a", CraftCompiler.Architecture.arm64).signature,
        )
