import unittest
import tempfile

from CraftDebug import craftDebug
import CraftTestBase
from CraftOS.osutils import OsUtils

class OsUtilsTest(CraftTestBase.CraftTestBase):

    def test_rm(self):
        _, fileName = tempfile.mkstemp()
        OsUtils.rm(fileName)

    def test_rmDir(self):
        dirName = tempfile.mkdtemp()
        OsUtils.rmDir(dirName)

if __name__ == '__main__':
    unittest.main()
