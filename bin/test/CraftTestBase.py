import os
import tempfile
import unittest

import CraftConfig
from CraftDebug import craftDebug


class CraftTestBase(unittest.TestCase):
    def setUp(self):
        craftDebug.setVerbose(int(os.environ["EMERGE_TEST_VERBOSITY"]))
        self.kdeRoot = tempfile.TemporaryDirectory()
        craftRoot = os.path.normpath(os.path.join(os.path.split(__file__)[0], "..", "..", ".."))
        CraftConfig.craftSettings = CraftConfig.CraftConfig(os.path.join(craftRoot, "craft", "kdesettings.ini"))
        CraftConfig.CraftStandardDirs.allowShortpaths(False)
        CraftConfig.CraftStandardDirs._pathCache().clear()
        CraftConfig.CraftStandardDirs._pathCache()["EMERGEROOT"] = self.kdeRoot.name
        os.environ["KDEROOT"] = self.kdeRoot.name
        CraftConfig.craftSettings.set("General", "Portages", os.path.join(craftRoot, "craft", "portage"))
        CraftConfig.craftSettings.set("Compile", "BuildType", "RelWithDebInfo")

    def tearDown(self):
        del self.kdeRoot
