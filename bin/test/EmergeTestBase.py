import unittest
import tempfile
import os

import EmergeConfig
import EmergeDebug

class EmergeTestBase(unittest.TestCase):

    def setUp(self):
        EmergeDebug.setVerbose(int(os.environ["EMERGE_TEST_VERBOSITY"]))
        self.kdeRoot = tempfile.TemporaryDirectory()
        emergeRoot = os.path.normpath(os.path.join(os.path.split(__file__)[0], "..", "..", ".."))
        EmergeConfig.emergeSettings = EmergeConfig.EmergeConfig(os.path.join(emergeRoot, "emerge", "kdesettings.ini"))
        EmergeConfig.EmergeStandardDirs.allowShortpaths(False)
        EmergeConfig.EmergeStandardDirs._pathCache().clear()
        EmergeConfig.EmergeStandardDirs._pathCache()["EMERGEROOT"] = self.kdeRoot.name
        os.environ["KDEROOT"] = self.kdeRoot.name
        EmergeConfig.emergeSettings.set("General", "EMERGE_PORTAGE_ROOT", os.path.join(emergeRoot, "emerge", "portage") )
        EmergeConfig.emergeSettings.set("Compile","BuildType", "RelWithDebInfo")

    def tearDown(self):
        del self.kdeRoot