import os
import tempfile
import unittest

import CraftConfig
from CraftDebug import craftDebug
import InstallDB

class CraftTestBase(unittest.TestCase):
    def setUp(self):
        craftDebug.setVerbose(1)
        self.kdeRoot = tempfile.TemporaryDirectory()
        craftRoot = os.path.normpath(os.path.join(os.path.split(__file__)[0], "..", "..", ".."))
        CraftConfig.craftSettings = CraftConfig.CraftConfig(os.path.join(craftRoot, "craft", "kdesettings.ini"))
        CraftConfig.CraftStandardDirs.allowShortpaths(False)
        CraftConfig.CraftStandardDirs._pathCache().clear()
        CraftConfig.CraftStandardDirs._pathCache()["EMERGEROOT"] = self.kdeRoot.name
        os.environ["KDEROOT"] = self.kdeRoot.name
        CraftConfig.craftSettings.set("General", "Portages", os.path.join(craftRoot, "craft", "portage"))
        CraftConfig.craftSettings.set("Compile", "BuildType", "RelWithDebInfo")
        if hasattr(InstallDB, "installdb"):
            del InstallDB.installdb
        InstallDB.installdb = InstallDB.InstallDB(os.path.join(self.kdeRoot.name, "test.db"))

    def tearDown(self):
        InstallDB.installdb.connection.close()
        del InstallDB.installdb
        del self.kdeRoot
