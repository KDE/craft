import importlib.util
from argparse import Namespace
from pathlib import Path
from unittest import TestCase, mock


def importCraftBootstrap():
    craftRoot = Path(__file__).resolve().parents[2]
    spec = importlib.util.spec_from_file_location("CraftBootstrap", craftRoot / "setup" / "CraftBootstrap.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestCraftBootstrap(TestCase):
    def setUp(self):
        self.bootstrap = importCraftBootstrap()

    def testDefaultMacArchitectureDetectsArm64(self):
        self.assertEqual(self.defaultMacArchitecture("arm64", "RELEASE_ARM64_T8112"), "arm64")

    def testDefaultMacArchitectureDetectsRosettaOnArm64(self):
        self.assertEqual(self.defaultMacArchitecture("x86_64", "RELEASE_ARM64_T8112"), "arm64")

    def testDefaultMacArchitectureDetectsX8664(self):
        self.assertEqual(self.defaultMacArchitecture("x86_64", "RELEASE_X86_64"), "x86_64")

    def testGetAbiDefaultsToDetectedMacArchitecture(self):
        with (
            mock.patch.object(self.bootstrap.CraftBootstrap, "isWin", return_value=False),
            mock.patch.object(self.bootstrap.CraftBootstrap, "isAndroid", return_value=False),
            mock.patch.object(self.bootstrap.CraftBootstrap, "isUnix", return_value=True),
            mock.patch.object(self.bootstrap.CraftBootstrap, "isMac", return_value=True),
            mock.patch.object(self.bootstrap.CraftBootstrap, "defaultMacArchitecture", return_value="arm64"),
        ):
            self.assertEqual(self.bootstrap.getABI(Namespace(use_defaults=True)), "macos-clang-arm64")

    def defaultMacArchitecture(self, machine, version):
        uname = mock.Mock(version=version)
        with (
            mock.patch.object(self.bootstrap.platform, "machine", return_value=machine),
            mock.patch.object(self.bootstrap.platform, "uname", return_value=uname),
        ):
            return self.bootstrap.CraftBootstrap.defaultMacArchitecture()
