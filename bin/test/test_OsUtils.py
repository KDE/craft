import os
import subprocess
import tempfile
import threading
import unittest

import CraftTestBase
import utils
from CraftCore import CraftCore
from CraftOS.OsDetection import OsDetection
from CraftOS.osutils import LockFile, OsUtils


class OsUtilsTest(CraftTestBase.CraftTestBase):
    def test_rm(self):
        fd, fileName = tempfile.mkstemp()
        os.close(fd)
        OsUtils.rm(fileName)

    def test_rmDir(self):
        dirName = tempfile.mkdtemp()
        OsUtils.rmDir(dirName)

    def test_killProcess(self):
        # TODO: find a better test app than the cmd windows
        if OsDetection.isWin():
            with tempfile.TemporaryDirectory() as tmp1:
                with tempfile.TemporaryDirectory() as tmp2:
                    test1 = os.path.join(tmp1, "craft_test.exe")
                    test2 = os.path.join(tmp2, "craft_test.exe")
                    cmd = CraftCore.cache.findApplication("cmd")
                    self.assertEqual(utils.copyFile(cmd, test1, linkOnly=False), True)
                    self.assertEqual(utils.copyFile(cmd, test2, linkOnly=False), True)
                    process = subprocess.Popen([test1, "/K"], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
                    process2 = subprocess.Popen([test2, "/K"], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
                    try:
                        self.assertEqual(process.poll(), None)
                        self.assertEqual(process2.poll(), None)
                        self.assertEqual(OsUtils.killProcess("craft_test", tmp2), True)
                        self.assertEqual(process.poll(), None)
                        # ensure that process 2 was killed
                        self.assertNotEqual(process2.poll(), None)
                    except subprocess.SubprocessError as e:
                        CraftCore.log.warning(e)
                    finally:
                        process.kill()
                        process2.kill()
                        process.wait()
                        process2.wait()

    def test_LockFile(self):
        if OsDetection.isUnix():
            lock = LockFile("foo")
            print("start")
            lock.lock()

            def _delayedUnlock():
                print("unlock1")
                lock.unlock()

            threading.Timer(5, _delayedUnlock).start()
            with LockFile("foo"):
                print("locked lock2")
            print("end")


if __name__ == "__main__":
    unittest.main()
