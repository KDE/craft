import CraftTestBase

from Blueprints.CraftVersion import *
from options import *

import configparser


class TestUserOptions(CraftTestBase.CraftTestBase):
    def _prepare(self, options=None):
        path = os.path.join(self.kdeRoot.name, "BlueprintSettings.ini")
        del UserOptions.UserOptionsSingleton._instance
        UserOptions.UserOptionsSingleton._instance = None

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

        return UserOptions.instance()

    def test(self):
        package = CraftPackageObject.get("dev-utils/7zip")
        # init the package
        package.subinfo.registerOptions()
        instance = self._prepare({
            package.path : {"version":"5", "ignored":"True", "customeOptionInt":"5"},
            "dev-util"   : {"args":"Foo"}})

        o = UserOptions.get(package)

        self.assertEqual(UserOptions.instance().settings["#Core"]["needsShortPath"], "False")

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

    def testOptions(self):
        UserOptions.setOptions(["qt-apps/gammaray.gammarayProbeOnly = True", "qt-apps/gammaray.disableGammarayBuildCliInjector = True"])
        package = CraftPackageObject.get("qt-apps/gammaray")
        # init the package
        package.subinfo.registerOptions()
        option = UserOptions.get(package)
        self.assertEqual(option.gammarayProbeOnly, True)
        self.assertEqual(option.disableGammarayBuildCliInjector, True)

