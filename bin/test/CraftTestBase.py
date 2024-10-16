import os
import tempfile
import unittest
from pathlib import Path

import CraftConfig
import CraftStandardDirs
import InstallDB
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore
from options import UserOptions


class CraftTestBase(unittest.TestCase):
    def setUp(self):
        CraftCore.debug.setVerbose(int(os.getenv("CRAFT_TEST_VERBOSITY")))
        self.kdeRoot = tempfile.TemporaryDirectory()
        CraftCore.settings = CraftConfig.CraftConfig(
            os.path.join(os.path.normpath(os.path.join(os.path.split(__file__)[0], "..", "..", "..")), "craft", "CraftSettings.ini.template")
        )

        CraftCore.standardDirs = CraftStandardDirs.CraftStandardDirs(self.kdeRoot.name)
        os.makedirs(CraftCore.standardDirs.etcDir())

        if "CRAFT_TEST_BLUEPRINTS_ROOT" in os.environ:
            blueprintRoot = Path(os.environ["CRAFT_TEST_BLUEPRINTS_ROOT"]).resolve()
            if not blueprintRoot.exists():
                self.fail(f"blueprintRoot: {blueprintRoot} does not exist")
            CraftCore.settings.set("Blueprints", "BlueprintRoot", str(blueprintRoot))

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
        CraftCore.log.info(f"BlueprintRoot: {CraftCore.standardDirs.blueprintRoot()}")
        CraftCore.log.info(f"BlueprintsRootDirectories {CraftPackageObject.rootDirectories()}")
        CraftCore.log.info(f"BlueprintSettings: {CraftCore.settings.get('Blueprints', 'Settings')}")
        CraftCore.log.info(f"dbPath: {dbPath}")

        del UserOptions.UserOptionsSingleton._instance
        UserOptions.UserOptionsSingleton._instance = None

    def tearDown(self):
        CraftCore.installdb.connection.close()
        del CraftCore.installdb
        del UserOptions.UserOptionsSingleton._instance
        UserOptions.UserOptionsSingleton._instance = None
        del self.kdeRoot
