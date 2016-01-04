import unittest
import tempfile
import os

import EmergeConfig
import EmergeDebug

class EmergeTestBase(unittest.TestCase):

    def setUp(self):
        EmergeDebug.setVerbose(int(os.environ["EMERGE_TEST_VERBOSITY"]))
        self.kdeRoot = tempfile.TemporaryDirectory()
        EmergeConfig.EmergeStandardDirs.allowShortpaths(False)
        EmergeConfig.EmergeStandardDirs._pathCache()["EMERGEROOT"] = self.kdeRoot.name
        os.environ["KDEROOT"] = self.kdeRoot.name

    def tearDown(self):
        del self.kdeRoot