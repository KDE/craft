import os
import tempfile
import unittest

import CraftConfig
import CraftStandardDirs
import InstallDB
from CraftCore import CraftCore
from options import UserOptions


class CraftTestBase(unittest.TestCase):
    def setUp(self):
        CraftCore.debug.setVerbose(int(os.getenv("CRAFT_TEST_VERBOSITY")))
        if "CRAFT_TEST_BLUEPRINTS_ROOT" not in os.environ:
            blueprintsDir = CraftCore.standardDirs.blueprintRoot()
        else:
            blueprintsDir = os.environ["CRAFT_TEST_BLUEPRINTS_ROOT"]
        self.kdeRoot = tempfile.TemporaryDirectory()
        craftRoot = os.path.normpath(os.path.join(os.path.split(__file__)[0], "..", "..", ".."))
        oldSettings = CraftCore.settings
        CraftCore.settings = CraftConfig.CraftConfig(os.path.join(craftRoot, "craft", "CraftSettings.ini.template"))

        CraftCore.standardDirs = CraftStandardDirs.CraftStandardDirs(self.kdeRoot.name)
        os.makedirs(CraftCore.standardDirs.etcDir())
        CraftCore.settings.set("Blueprints", "BlueprintRoot", blueprintsDir)
        CraftCore.settings.set("Compile", "BuildType", "RelWithDebInfo")
        CraftCore.settings.set(
            "Blueprints",
            "Settings",
            os.path.join(self.kdeRoot.name, "BlueprintSettings.ini"),
        )
        if hasattr(CraftCore, "installdb"):
            del CraftCore.installdb
        CraftCore.installdb = InstallDB.InstallDB(os.path.join(self.kdeRoot.name, "test.db"))

        del UserOptions.UserOptionsSingleton._instance
        UserOptions.UserOptionsSingleton._instance = None

    def tearDown(self):
        CraftCore.installdb.connection.close()
        del CraftCore.installdb
        del UserOptions.UserOptionsSingleton._instance
        UserOptions.UserOptionsSingleton._instance = None
        del self.kdeRoot
