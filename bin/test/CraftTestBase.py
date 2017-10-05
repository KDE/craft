import os
import tempfile
import unittest

import CraftConfig
import CraftStandardDirs
from CraftCore import CraftCore
import InstallDB

class CraftTestBase(unittest.TestCase):
    def setUp(self):
        CraftCore.debug.setVerbose(1)
        self.kdeRoot = tempfile.TemporaryDirectory()
        craftRoot = os.path.normpath(os.path.join(os.path.split(__file__)[0], "..", "..", ".."))
        CraftConfig.craftSettings = CraftConfig.CraftConfig(os.path.join(craftRoot, "craft", "CraftSettings.ini.template"))
        CraftCore.settings = CraftConfig.craftSettings
        CraftCore.standardDirs = CraftStandardDirs.CraftStandardDirs()
        CraftStandardDirs.CraftStandardDirs.allowShortpaths(False)
        CraftConfig.craftSettings.set("Blueprints", "Locations", os.path.join(craftRoot, "craft", "blueprints"))
        CraftConfig.craftSettings.set("Blueprints", "BlueprintRoot", os.path.join(craftRoot, "etc", "blueprints", "locations"))
        CraftConfig.craftSettings.set("Compile", "BuildType", "RelWithDebInfo")
        if hasattr(InstallDB, "installdb"):
            del InstallDB.installdb
        InstallDB.installdb = InstallDB.InstallDB(os.path.join(self.kdeRoot.name, "test.db"))

    def tearDown(self):
        InstallDB.installdb.connection.close()
        del InstallDB.installdb
        del self.kdeRoot
