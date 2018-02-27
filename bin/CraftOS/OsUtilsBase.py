import abc
import os
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
    def toWindowsPath(path : str) -> str:
        path = os.path.normpath(path)
        return path.replace("/", "\\")

    @staticmethod
    def toUnixPath(path : str) -> str:
        path = os.path.normpath(path)
        return path.replace("\\", "/")

    @staticmethod
    def toMSysPath(path):
        path = OsUtilsBase.toUnixPath(path)
        drive, path = os.path.splitdrive(path)
        if drive:
            return f"/{drive[0].lower()}{path}"
        return path

    @staticmethod
    def toNativePath(path : str) -> str:
        """Return a native path"""
        pass

    @staticmethod
    def enableAnsiColors():
        os.environ["CLICOLOR_FORCE"] = "1"
        os.environ["CLICOLOR"] = "1"
        # TODO: cleanup
        os.environ["CFLAGS"] = "-fdiagnostics-color=always"
        os.environ["CXXFLAGS"] = "-fdiagnostics-color=always"
