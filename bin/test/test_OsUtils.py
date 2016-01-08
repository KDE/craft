import unittest
import tempfile

import EmergeDebug
import EmergeTestBase
from EmergeOS.osutils import OsUtils

class OsUtilsTest(EmergeTestBase.EmergeTestBase):

    def test_rm(self):
        _, fileName = tempfile.mkstemp()
        OsUtils.rm(fileName)

    def test_rmDir(self):
        dirName = tempfile.mkdtemp()
        OsUtils.rmDir(dirName)

if __name__ == '__main__':
    unittest.main()
