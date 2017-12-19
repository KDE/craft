import CraftTestBase

from Blueprints.CraftVersion import *
from options import *

import configparser


class TestCraftVersion(CraftTestBase.CraftTestBase):
    def _prepare(self, options):
        path = UserOptions.instance().path
        del UserOptions.UserOptionsSingleton._instance
        UserOptions.UserOptionsSingleton._instance = None

        settings = configparser.ConfigParser(allow_no_value=True)
        settings.optionxform = str

        for package, values in options.items():
            settings.add_section(package)
            section = settings[package]
            for k, v in values.items():
                section[k] = v

        with open(path, "wt+") as ini:
            settings.write(ini)

        return UserOptions.instance()

    def test(self):
        package = CraftPackageObject.get("dev-util/7zip")
        instance = self._prepare({
            package.path : {"version":"5", "ignored":"True", "customeOptionInt":"5"},
            "dev-util"   : {"args":"Foo"}})

        o = UserOptions.get(package)

        self.assertEqual(type(o.customeOptionInt), str)
        self.assertEqual(o.customeOptionInt, "5")
        o.registerOption("customeOptionInt", 42)
        self.assertEqual(type(o.customeOptionInt), int)
        self.assertEqual(o.customeOptionInt, 5)

        self.assertEqual(o.ignored, True)
        self.assertEqual(o.version, "5")
        self.assertEqual(o.args, "Foo")

        self.assertEqual(o.not_existing, None)
        o.registerOption("not_existing", True)
        self.assertEqual(o.not_existing, None)
