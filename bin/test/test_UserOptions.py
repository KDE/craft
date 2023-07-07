import configparser

import CraftTestBase
from Blueprints.CraftVersion import *
from options import *


class TestUserOptions(CraftTestBase.CraftTestBase):
    def _prepare(self, options=None):
        path = CraftCore.settings.get("Blueprints", "Settings")

        settings = configparser.ConfigParser(allow_no_value=True)
        settings.optionxform = str

        if options:
            for package, values in options.items():
                settings.add_section(package)
                section = settings[package]
                for k, v in values.items():
                    section[k] = v

            with open(path, "wt+") as ini:
                settings.write(ini)

        # reload the settings
        del UserOptions.UserOptionsSingleton._instance
        UserOptions.UserOptionsSingleton._instance = None
        return UserOptions.instance()

    def test(self):
        package = CraftPackageObject.get("dev-utils/7zip")
        # init the package
        package.subinfo.registerOptions()
        instance = self._prepare(
            {
                package.path: {
                    "version": "5",
                    "ignored": "True",
                    "customeOptionInt": "5",
                },
                "dev-utils": {"args": "Foo", "featureArguments": 'Foo bar "-DQuotedString=This is quoted"'},
            }
        )

        o = UserOptions.get(package)

        self.assertEqual(type(o.customeOptionInt), str)
        self.assertEqual(o.customeOptionInt, "5")
        o.registerOption("customeOptionInt", 42)
        self.assertEqual(type(o.customeOptionInt), int)
        self.assertEqual(o.customeOptionInt, 5)

        self.assertEqual(o.ignored, True)
        self.assertEqual(o.version, "5")
        self.assertEqual(o.args.get(), str(Arguments(["Foo"])))
        self.assertEqual(o.featureArguments.get(), str(Arguments(["Foo", "bar", "-DQuotedString=This is quoted"])))
        self.assertEqual((o.featureArguments + ["1", "2", "3"]).get(), 'Foo bar "-DQuotedString=This is quoted" 1 2 3')
        self.assertEqual((o.featureArguments + ["1", "2", "3"]).get(), str(Arguments('Foo bar "-DQuotedString=This is quoted"') + Arguments(["1", "2", "3"])))

        self.assertEqual(o.not_existing, None)
        o.registerOption("not_existing", True)
        self.assertEqual(o.not_existing, None)

    def testOptions(self):
        package = CraftPackageObject.get("test-blueprint")
        # initialize subinfo and options
        package.subinfo.registerOptions()
        option = UserOptions.get(package)
        self.assertEqual(option.thetruth, False)
        self.assertEqual(option.name, "Something")
        UserOptions.setOptions(
            [
                "test-blueprint.thetruth = True",
                "test-blueprint.name = TestTitle",
            ]
        )
        self.assertEqual(option.thetruth, True)
        self.assertEqual(option.name, "TestTitle")
