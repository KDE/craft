import importlib

import CraftConfig
import CraftTestBase
from Blueprints import CraftPackageObject


class CraftBlueprintTest(CraftTestBase.CraftTestBase):
    def blueprintTest(self, compiler):
        CraftConfig.CraftCore.settings.set("General", "ABI", compiler)

        importlib.reload(CraftPackageObject)  # clear cache
        installable = CraftPackageObject.CraftPackageObject.installables()
        for _p in installable:
            _p.instance


class TestAPI(CraftBlueprintTest):
    def test_mingw_x86(self):
        self.blueprintTest("windows-mingw_86-gcc")

    def test_mingw_x64(self):
        self.blueprintTest("windows-mingw_64-gcc")

    def test_msvc2015_x86(self):
        self.blueprintTest("windows-msvc2015_86-cl")

    def test_msvc2015_x64(self):
        self.blueprintTest("windows-msvc2015_64-cl")
