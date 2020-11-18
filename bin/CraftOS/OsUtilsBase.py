import abc
import os
from pathlib import Path
import platform

import sys

from CraftOS.OsDetection import OsDetection


class OsUtilsBase(OsDetection, metaclass=abc.ABCMeta):
    @abc.abstractstaticmethod
    def rm(path, force=False):
        """ Removes a file"""
        pass

    @abc.abstractstaticmethod
    def rmDir(path, force=False):
        """ Removes a file"""
        pass

    @abc.abstractstaticmethod
    def getFileAttributes(path):
        """ Returns the attributes"""
        pass

    @abc.abstractstaticmethod
    def removeReadOnlyAttribute(path):
        """ Removes the readonly flag"""
        pass

    def setConsoleTitle(title):
        """ Set the console title """
        return True

    @staticmethod
    def supportsSymlinks() -> bool:
        return True

    @staticmethod
    def toWindowsPath(path : str) -> Path:
        if not path:
            return None
        return Path(path)

    @staticmethod
    def toUnixPath(path : str) -> str:
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
    def toNativePath(path : str) -> str:
        """Return a native path"""
        pass

    @staticmethod
    def killProcess(name : str="*", prefix : str=None) -> bool:
        pass

    @staticmethod
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
