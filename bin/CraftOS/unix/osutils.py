import fcntl
import os
import shutil
import sys
import time
from pathlib import Path
from typing import Optional

import CraftOS.OsUtilsBase
from CraftCore import CraftCore


class OsUtils(CraftOS.OsUtilsBase.OsUtilsBase):
    InDocker = None

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

    @staticmethod
    def toNativePath(path: str) -> str:
        return str(OsUtils.toUnixPath(path))

    @staticmethod
    def killProcess(name: str = "*", prefix: Optional[str] = None) -> bool:
        CraftCore.log.warning("killProcess is not implemented")
        return True

    @staticmethod
    def detectDocker() -> bool:
        if OsUtils.InDocker is None:
            if Path("/.dockerenv").exists():
                OsUtils.InDocker = True
            if Path("/run/.containerenv").exists():
                # This is really for Podman - but given the behaviour changes we need to make are the same it should be fine
                OsUtils.InDocker = True
            if OsUtils.InDocker is None:
                with open("/proc/self/cgroup", "rt") as f:
                    lines = f.read()
                    # a false positive should not really hurt...
                    OsUtils.InDocker = ":/docker/" in lines
                    CraftCore.log.debug(f"detectDocker: {OsUtils.InDocker} {lines}")
        return OsUtils.InDocker


class LockFile(CraftOS.OsUtilsBase.LockFileBase):
    def __init__(self, name):
        super().__init__(name)
        self.__lockFileName = f"/tmp/craftlock-{self.name}"
        self.__lockFile = None

    def lock(self):
        while True:
            try:
                if not self.__lockFile:
                    self.__lockFile = os.open(self.__lockFileName, os.O_WRONLY | os.O_CREAT, 0o777)
                fcntl.flock(self.__lockFile, fcntl.LOCK_EX | fcntl.LOCK_NB)
                self._locked = True
                break
            except IOError as e:
                CraftCore.log.info(f"{self.__lockFileName} is locked waiting: {e}")
                time.sleep(10)

    def unlock(self):
        if self._locked:
            fcntl.flock(self.__lockFile, fcntl.LOCK_UN)
            self._locked = False
        if self.__lockFile:
            os.close(self.__lockFile)
            self.__lockFile = None
