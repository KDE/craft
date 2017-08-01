import os
import shutil
import sys

import CraftOS.OsUtilsBase
from CraftDebug import craftDebug


class OsUtils(CraftOS.OsUtilsBase.OsUtilsBase):
    @staticmethod
    def rm(path, force=False):
        craftDebug.log.debug("deleting file %s" % path)
        try:
            os.remove(path)
            return True
        except OSError as e:
            craftDebug.log.warning("could not delete file %s: %s" % (path, e))
            return False

    @staticmethod
    def rmDir(path, force=False):
        craftDebug.log.debug("deleting directory %s" % path)
        try:
            shutil.rmtree(path)
            return True
        except OSError:
            return OsUtils.rm(path, force)
        return False

    @staticmethod
    def isLink(path):
        return os.path.islink(path)

    @staticmethod
    def removeReadOnlyAttribute(path):
        return False

    @staticmethod
    def setConsoleTitle(title):
        sys.stdout.buffer.write(b"\x1b]0;")
        sys.stdout.buffer.write(bytes(title, "UTF-8"))
        sys.stdout.buffer.write(b"\x07")
        sys.stdout.flush()
        return True
