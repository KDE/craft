import EmergeOS.OsUtilsBase
import EmergeDebug
import shutil
import os

class OsUtils(EmergeOS.OsUtilsBase.OsUtilsBase):

    @staticmethod
    def rm(path, force=False):
        EmergeDebug.debug("deleting file %s" % path, 3)
        try:
            os.remove(path)
            return True
        except OSError as e:
            EmergeDebug.warning("could not delete file %s: %s" % (path, e))
            return False

    @staticmethod
    def rmDir(path, force=False):
        EmergeDebug.debug("deleting directory %s" % path, 3)
        try:
            shutil.rmtree(path)
            return True
        except OSError as e:
            EmergeDebug.warning("could not delete directory %s: %s" % (path, e))
            return False
        return False

    @staticmethod
    def removeReadOnlyAttribute(path):
        return False

    @staticmethod
    def setConsoleTitle(title):
        return True # pass
