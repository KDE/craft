import CraftTestBase
from Blueprints.CraftVersion import CraftVersion
from Blueprints.distutils_version import StrictVersion
from CraftCore import CraftCore


class TestCraftVersion(CraftTestBase.CraftTestBase):
    def test_str(self):
        self.assertEqual(str(CraftVersion("5.8.1")), "5.8.1")

    def test_compare(self):
        for small, big in [
            (CraftVersion("5.8.0"), CraftVersion("5.8.1")),
            (CraftVersion("5.8.0"), CraftVersion("5.8.0-1")),
            (CraftVersion("1.0.2j"), CraftVersion("1.0.2k")),
            (CraftVersion("v1.0.2j"), CraftVersion("1.0.2k")),
            (CraftVersion("master"), CraftVersion("5.8.1")),
            (CraftVersion("dev"), CraftVersion("5.8.1")),
            (CraftVersion("1_59_1"), CraftVersion("1_65_1")),
            (CraftVersion("1_59"), CraftVersion("1_65_1")),
            (CraftVersion("master-2017.12.14"), CraftVersion("master-2017.12.15")),
            (CraftVersion("2017.12-2017.12.14"), CraftVersion("2017.12-2017.12.15")),
            (CraftVersion("Applications/16.12"), CraftVersion("Applications/16.13")),
        ]:
            if CraftCore.debug.verbose() > 2:
                print(f"{small.version} {big.version}")
            self.assertEqual(small, small)
            self.assertEqual(big, big)
            self.assertLess(small, big)
            self.assertGreater(big, small)

    def test_tag(self):
        for a, b in [(CraftVersion("v1.0.2j"), CraftVersion("1.0.2j"))]:
            self.assertEqual(a.version, b.version)

    def test_compareBranch(self):
        self.assertNotEqual(CraftVersion("master"), CraftVersion("dev"))

    def test_strict(self):
        self.assertEqual(CraftVersion("5.8.1").strictVersion, StrictVersion("5.8.1"))
        self.assertEqual(CraftVersion("1.0.2j").strictVersion, StrictVersion("1.0.29"))
        self.assertEqual(CraftVersion("v1.0.2j").strictVersion, StrictVersion("1.0.29"))
        self.assertEqual(CraftVersion("1.0.2.9").strictVersion, StrictVersion("1.0.29"))

    def test_fail(self):
        # TODO: how to parse git versiosns
        self.assertEqual(CraftVersion("Applications/16.12").strictVersion, StrictVersion("0.0.0"))
        self.assertEqual(CraftVersion("master").strictVersion, StrictVersion("0.0.0"))
