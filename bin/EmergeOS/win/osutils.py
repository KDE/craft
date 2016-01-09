import EmergeOS.OsUtilsBase
import EmergeDebug
import ctypes
import os

class OsUtils(EmergeOS.OsUtilsBase.OsUtilsBase):

    @staticmethod
    def rm(path, force=False):
        EmergeDebug.debug("deleting file %s" % path, 3)
        if force:
            OsUtils.removeReadOnlyAttribute(path)
        return ctypes.windll.kernel32.DeleteFileW(path) != 0

    @staticmethod
    def rmDir(path, force=False):
        EmergeDebug.debug("deleting directory %s" % path, 3)
        if force:
            OsUtils.removeReadOnlyAttribute(path)
        return ctypes.windll.kernel32.RemoveDirectoryW(path) != 0

    @staticmethod
    def getFileAttributes(path):
        return ctypes.windll.kernel32.GetFileAttributesW(path)

    @staticmethod
    def removeReadOnlyAttribute(path):
        attributes =  OsUtils.getFileAttributes(path)
        return ctypes.windll.kernel32.SetFileAttributesW(path,attributes & ~ 0x1) != 0

    @staticmethod
    def setConsoleTitle(title):
        return ctypes.windll.kernel32.SetConsoleTitleW(title) != 0
