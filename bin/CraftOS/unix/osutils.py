import os
import shutil
import sys

import CraftOS.OsUtilsBase
from CraftCore import CraftCore


class OsUtils(CraftOS.OsUtilsBase.OsUtilsBase):
    @staticmethod
    def rm(path, force=False):
        CraftCore.log.debug("deleting file %s" % path)
        try:
            os.remove(path)
            return True
        except OSError as e:
            CraftCore.log.warning("could not delete file %s: %s" % (path, e))
            return False

    @staticmethod
    def rmDir(path, force=False):
        CraftCore.log.debug("deleting directory %s" % path)
        try:
            shutil.rmtree(path)
            return True
        except (OSError, PermissionError):
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

    @staticmethod
    def toNativePath(path : str) -> str:
        return OsUtils.toUnixPath(path)

    @staticmethod
    def killProcess(name : str="*", prefix : str=None) -> bool:
        CraftCore.log.warning("killProcess is not implemented")
        return True
