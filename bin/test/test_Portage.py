import importlib

import CraftTestBase

import CraftConfig
import CraftPackageObject


class CraftPortageTest(CraftTestBase.CraftTestBase):
    def portageTest(self, compiler):
        CraftConfig.craftSettings.set("General", "ABI", compiler)

        importlib.reload(CraftPackageObject)  # clear cache
        installable = CraftPackageObject.CraftPackageObject.installables()
        for _p in installable:
            _p.instance


class TestAPI(CraftPortageTest):
    def test_mingw_x86(self):
        self.portageTest("windows-mingw_86-gcc")

    def test_mingw_x64(self):
        self.portageTest("windows-mingw_64-gcc")

    def test_msvc2015_x86(self):
        self.portageTest("windows-msvc2015_86-cl")

    def test_msvc2015_x64(self):
        self.portageTest("windows-msvc2015_64-cl")
