import CraftTestBase
from CraftCompiler import CraftCompiler, CraftCompilerSignature
from CraftCore import CraftCore


class TestCompilerSeignature(CraftTestBase.CraftTestBase):
    def test(self):
        self.assertEqual(
            CraftCompilerSignature.parseAbi("windows-msvc2019_64-cl", CraftCore.compiler.hostSignature).signature,
            CraftCompilerSignature(
                CraftCompiler.Platforms.Windows, CraftCompiler.Compiler.CL, "msvc2019", CraftCompiler.Architecture.x86_64, CraftCore.compiler.hostSignature
            ).signature,
        )
        self.assertEqual(
            CraftCompilerSignature.parseAbi("windows-cl-msvc2019-x86_64", CraftCore.compiler.hostSignature).signature,
            CraftCompilerSignature(
                CraftCompiler.Platforms.Windows, CraftCompiler.Compiler.CL, "msvc2019", CraftCompiler.Architecture.x86_64, CraftCore.compiler.hostSignature
            ).signature,
        )
        self.assertEqual(
            CraftCompilerSignature.parseAbi("windows-gcc-x86_64", CraftCore.compiler.hostSignature).signature,
            CraftCompilerSignature(
                CraftCompiler.Platforms.Windows, CraftCompiler.Compiler.GCC, None, CraftCompiler.Architecture.x86_64, CraftCore.compiler.hostSignature
            ).signature,
        )
        self.assertEqual(
            CraftCompilerSignature.parseAbi("macos-clang-arm64", CraftCore.compiler.hostSignature).signature,
            CraftCompilerSignature(
                CraftCompiler.Platforms.MacOS, CraftCompiler.Compiler.CLANG, None, CraftCompiler.Architecture.arm64, CraftCore.compiler.hostSignature
            ).signature,
        )
        self.assertEqual(
            CraftCompilerSignature.parseAbi("android-arm64-clang", CraftCore.compiler.hostSignature).signature,
            CraftCompilerSignature(
                CraftCompiler.Platforms.Android, CraftCompiler.Compiler.CLANG, None, CraftCompiler.Architecture.arm64, CraftCore.compiler.hostSignature
            ).signature,
        )
        self.assertEqual(
            CraftCompilerSignature.parseAbi("android-clang-arm", CraftCore.compiler.hostSignature).signature,
            CraftCompilerSignature(
                CraftCompiler.Platforms.Android, CraftCompiler.Compiler.CLANG, None, CraftCompiler.Architecture.arm, CraftCore.compiler.hostSignature
            ).signature,
        )
        self.assertEqual(
            CraftCompilerSignature.parseAbi("android-clang-arm64", CraftCore.compiler.hostSignature).signature,
            CraftCompilerSignature(
                CraftCompiler.Platforms.Android, CraftCompiler.Compiler.CLANG, None, CraftCompiler.Architecture.arm64, CraftCore.compiler.hostSignature
            ).signature,
        )
        self.assertEqual(
            CraftCompilerSignature.parseAbi("android-clang-x86_64", CraftCore.compiler.hostSignature).signature,
            CraftCompilerSignature(
                CraftCompiler.Platforms.Android, CraftCompiler.Compiler.CLANG, None, CraftCompiler.Architecture.x86_64, CraftCore.compiler.hostSignature
            ).signature,
        )
        self.assertEqual(
            CraftCompilerSignature.parseAbi("linux-64-gcc", CraftCore.compiler.hostSignature).signature,
            CraftCompilerSignature(
                CraftCompiler.Platforms.Linux, CraftCompiler.Compiler.GCC, None, CraftCompiler.Architecture.x86_64, CraftCore.compiler.hostSignature
            ).signature,
        )
        self.assertEqual(
            CraftCompilerSignature.parseAbi("linux-gcc-x86_64", CraftCore.compiler.hostSignature).signature,
            CraftCompilerSignature(
                CraftCompiler.Platforms.Linux, CraftCompiler.Compiler.GCC, None, CraftCompiler.Architecture.x86_64, CraftCore.compiler.hostSignature
            ).signature,
        )
