import abc
import os
from pathlib import Path
from typing import Optional

from CraftOS.OsDetection import OsDetection


class OsUtilsBase(OsDetection, metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def rm(path, force=False):
        """Removes a file"""
        pass

    @staticmethod
    @abc.abstractmethod
    def rmDir(path, force=False):
        """Removes a file"""
        pass

    @staticmethod
    @abc.abstractmethod
    def getFileAttributes(path):
        """Returns the attributes"""
        pass

    @staticmethod
    @abc.abstractmethod
    def removeReadOnlyAttribute(path):
        """Removes the readonly flag"""
        pass

    def setConsoleTitle(title):
        """Set the console title"""
        return True

    @staticmethod
    def supportsSymlinks() -> bool:
        return True

    @staticmethod
    def toWindowsPath(path: str) -> Path:
        if not path:
            return None
        return Path(path)

    @staticmethod
    def toUnixPath(path: str) -> str:
        if not path:
            return None
        return Path(path).as_posix()

    @staticmethod
    def toMSysPath(path) -> str:
        if not path:
            return None
        out = OsUtilsBase.toUnixPath(path)
        drive, path = os.path.splitdrive(out)
        if drive:
            return f"/{drive[0].lower()}{path}"
        return out

    @staticmethod
    @abc.abstractmethod
    def toNativePath(path: str) -> str:
        """Return a native path"""
        pass

    @staticmethod
    @abc.abstractmethod
    def killProcess(name: str = "*", prefix: Optional[str] = None) -> bool:
        pass

    @staticmethod
    @abc.abstractmethod
    def detectDocker() -> bool:
        pass


class LockFileBase(object, metaclass=abc.ABCMeta):
    def __init__(self, name):
        self.name = name
        self._locked = False

    @property
    def isLocked(self):
        return self._locked

    @abc.abstractmethod
    def lock(self):
        pass

    @abc.abstractmethod
    def unlock(self):
        pass

    def __enter__(self):
        self.lock()
        return self

    def __exit__(self, exc_type, exc_value, trback):
        self.unlock()
