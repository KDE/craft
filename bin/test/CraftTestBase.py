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
        CraftCore.settings = CraftConfig.CraftConfig(
            os.path.join(os.path.normpath(os.path.join(os.path.split(__file__)[0], "..", "..", "..")), "craft", "CraftSettings.ini.template")
        )

        CraftCore.standardDirs = CraftStandardDirs.CraftStandardDirs(self.kdeRoot.name)
        os.makedirs(CraftCore.standardDirs.etcDir())
        CraftCore.settings.set("Blueprints", "BlueprintRoot", CraftCore.standardDirs.blueprintRoot())
        CraftCore.settings.set("Compile", "BuildType", "RelWithDebInfo")
        CraftCore.settings.set(
            "Blueprints",
            "Settings",
            os.path.join(self.kdeRoot.name, "BlueprintSettings.ini"),
        )
        if hasattr(CraftCore, "installdb"):
            del CraftCore.installdb
        dbPath = os.path.join(self.kdeRoot.name, "test.db")

        CraftCore.installdb = InstallDB.InstallDB(dbPath)
        CraftCore.log.info(f"CraftRoot: {CraftCore.standardDirs.craftRoot()}")
        CraftCore.log.info(f"etcDir: {CraftCore.standardDirs.etcDir()}")
        CraftCore.log.info(f"BlueprintRoot: {blueprintsDir}")
        CraftCore.log.info(f"BlueprintSettings: {CraftCore.settings.get('Blueprints','Settings')}")
        CraftCore.log.info(f"dbPath: {dbPath}")

        del UserOptions.UserOptionsSingleton._instance
        UserOptions.UserOptionsSingleton._instance = None

    def tearDown(self):
        CraftCore.installdb.connection.close()
        del CraftCore.installdb
        del UserOptions.UserOptionsSingleton._instance
        UserOptions.UserOptionsSingleton._instance = None
        del self.kdeRoot
