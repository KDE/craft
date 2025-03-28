import CraftConfig
import CraftTestBase
from Blueprints import CraftDependencyPackage, CraftPackageObject
from options import UserOptions


class CraftBlueprintTest(CraftTestBase.CraftTestBase):
    def blueprintTest(self, compiler):
        CraftConfig.CraftCore.settings.set("General", "ABI", compiler)

        CraftPackageObject.__rootPackage = None
        CraftDependencyPackage._packageCache = dict()
        UserOptions.UserOptionsSingleton._instance = None
        CraftPackageObject.CraftPackageObject.root().allChildren()
        CraftDependencyPackage.CraftDependencyPackage(CraftPackageObject.CraftPackageObject.get("/")).getDependencies()


class TestAPI(CraftBlueprintTest):
    def test_mingw_x86(self):
        self.blueprintTest("windows-mingw_86-gcc")

    def test_mingw_x64(self):
        self.blueprintTest("windows-mingw_64-gcc")

    def test_msvc2019_x86(self):
        self.blueprintTest("windows-msvc2019_86-cl")

    def test_msvc2019_x64(self):
        self.blueprintTest("windows-msvc2019_64-cl")
