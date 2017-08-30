import os
import tempfile
import unittest

import CraftConfig
import CraftStandardDirs
from CraftDebug import craftDebug
import InstallDB

class CraftTestBase(unittest.TestCase):
    def setUp(self):
        craftDebug.setVerbose(1)
        self.kdeRoot = tempfile.TemporaryDirectory()
        craftRoot = os.path.normpath(os.path.join(os.path.split(__file__)[0], "..", "..", ".."))
        CraftConfig.craftSettings = CraftConfig.CraftConfig(os.path.join(craftRoot, "craft", "CraftSettings.ini.template"))
        CraftStandardDirs.CraftStandardDirs.allowShortpaths(False)
        CraftStandardDirs.CraftStandardDirs._pathCache().clear()
        CraftStandardDirs.CraftStandardDirs._pathCache()["EMERGEROOT"] = self.kdeRoot.name
        os.environ["KDEROOT"] = self.kdeRoot.name
        CraftConfig.craftSettings.set("Blueprints", "Locations", os.path.join(craftRoot, "craft", "blueprints"))
        CraftConfig.craftSettings.set("Compile", "BuildType", "RelWithDebInfo")
        if hasattr(InstallDB, "installdb"):
            del InstallDB.installdb
        InstallDB.installdb = InstallDB.InstallDB(os.path.join(self.kdeRoot.name, "test.db"))

    def tearDown(self):
        InstallDB.installdb.connection.close()
        del InstallDB.installdb
        del self.kdeRoot
