import subprocess
import os
import sys
import signal
import tempfile
import unittest

import CraftTestBase
import utils

from CraftOS.osutils import OsUtils
from CraftCore import CraftCore


class OsUtilsTest(CraftTestBase.CraftTestBase):
    def test_rm(self):
        _, fileName = tempfile.mkstemp()
        OsUtils.rm(fileName)

    def test_rmDir(self):
        dirName = tempfile.mkdtemp()
        OsUtils.rmDir(dirName)

    def test_killProcess(self):
        # TODO: find a better test app than the cmd windows
        with tempfile.TemporaryDirectory() as tmp1:
            with tempfile.TemporaryDirectory() as tmp2:
                test1 = os.path.join(tmp1, "craft_test.exe")
                test2 = os.path.join(tmp2, "craft_test.exe")
                cmd = CraftCore.cache.findApplication("cmd")
                self.assertEqual(utils.copyFile(cmd, test1, linkOnly=False), True)
                self.assertEqual(utils.copyFile(cmd, test2, linkOnly=False), True)
                process = subprocess.Popen([test1,"/K"], startupinfo=subprocess.CREATE_NEW_PROCESS_GROUP)
                process2 = subprocess.Popen([test2,"/K"], startupinfo=subprocess.CREATE_NEW_PROCESS_GROUP)
                try:
                    self.assertEqual(process.poll(), None)
                    self.assertEqual(process2.poll(), None)
                    self.assertEqual(OsUtils.killProcess("craft_test", tmp2), True)
                    self.assertEqual(process.poll(), None)
                    #ensure that process 2 was killed
                    self.assertNotEquals(process2.poll(), None)
                except subprocess.SubprocessError as e:
                    CraftCore.log.warning(e)
                finally:
                    process.kill()
                    process2.kill()
                    process.wait()
                    process2.wait()




if __name__ == '__main__':
    unittest.main()
