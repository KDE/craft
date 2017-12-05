import CraftTestBase

from Blueprints.CraftVersion import *


class TestCraftVersion(CraftTestBase.CraftTestBase):
    def test_str(self):
        self.assertEquals(str(CraftVersion("5.8.1")), "5.8.1")

    def test_compare(self):
        for small, big in [(CraftVersion("5.8.0"), CraftVersion("5.8.1")),
                           (CraftVersion("5.8.0"), CraftVersion("5.8.0-1")),
                           (CraftVersion("1.0.2j"), CraftVersion("1.0.2k")),
                           (CraftVersion("v1.0.2j"), CraftVersion("1.0.2k")),
                           (CraftVersion("5.8.1"), CraftVersion("master")),
                           (CraftVersion("5.8.1"), CraftVersion("dev")),
                           (CraftVersion("1_59_1"), CraftVersion("1_65_1")),
                           (CraftVersion("1_59"), CraftVersion("1_65_1")),
                           (CraftVersion("Applications/16.12"), CraftVersion("Applications/16.13"))]:
            self.assertEquals(small, small)
            self.assertEquals(big, big)
            self.assertLess(small, big)
            self.assertGreater(big, small)

    def test_tag(self):
        for a, b in [(CraftVersion("v1.0.2j"), CraftVersion("1.0.2j"))]:
            self.assertEquals(a.version, b.version)

    def test_compareBranch(self):
        self.assertEquals(CraftVersion("master"), CraftVersion("dev"))

    def test_strict(self):
        self.assertEquals(CraftVersion("5.8.1").strictVersion, StrictVersion("5.8.1"))
        self.assertEquals(CraftVersion("1.0.2j").strictVersion, StrictVersion("1.0.29"))
        self.assertEquals(CraftVersion("v1.0.2j").strictVersion, StrictVersion("1.0.29"))
        self.assertEquals(CraftVersion("1.0.2.9").strictVersion, StrictVersion("1.0.29"))

    def test_fail(self):
        # TODO: how to parse git versiosns
        self.assertEquals(CraftVersion("Applications/16.12").strictVersion, StrictVersion("0.0.0"))
        self.assertEquals(CraftVersion("master").strictVersion, StrictVersion("0.0.0"))
