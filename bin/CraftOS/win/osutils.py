import tempfile
import ctypes
import os
import platform
import subprocess

import CraftOS.OsUtilsBase
from CraftCore import CraftCore


class FileAttributes():
    # https://msdn.microsoft.com/en-us/library/windows/desktop/gg258117(v=vs.85).aspx
    FILE_ATTRIBUTE_READONLY = 0x1
    FILE_ATTRIBUTE_REPARSE_POINT = 0x400


class OsUtils(CraftOS.OsUtilsBase.OsUtilsBase):
    @staticmethod
    def rm(path, force=False):
        CraftCore.log.debug("deleting file %s" % path)
        if force:
            OsUtils.removeReadOnlyAttribute(path)
        return ctypes.windll.kernel32.DeleteFileW(path) != 0

    @staticmethod
    def rmDir(path, force=False):
        CraftCore.log.debug("deleting directory %s" % path)
        if force:
            OsUtils.removeReadOnlyAttribute(path)
        return ctypes.windll.kernel32.RemoveDirectoryW(path) != 0

    @staticmethod
    def isLink(path):
        return os.path.islink(path) \
               | OsUtils.getFileAttributes(path) & FileAttributes.FILE_ATTRIBUTE_REPARSE_POINT  # Detect a Junction

    @staticmethod
    def getFileAttributes(path):
        return ctypes.windll.kernel32.GetFileAttributesW(path)

    @staticmethod
    def removeReadOnlyAttribute(path):
        attributes = OsUtils.getFileAttributes(path)
        return ctypes.windll.kernel32.SetFileAttributesW(path,
                                                         attributes & ~ FileAttributes.FILE_ATTRIBUTE_READONLY) != 0

    @staticmethod
    def setConsoleTitle(title):
        return ctypes.windll.kernel32.SetConsoleTitleW(title) != 0

    @staticmethod
    def supportsSymlinks():
        with tempfile.TemporaryDirectory() as tmp:
            testFile = os.path.join(tmp, "CRAFT_LINK_TEST")
            return CraftCore.cache.getCommandOutput(f"cmd", f"/C mklink {testFile} {__file__}", testName="CRAFT_LINK_TEST")[0] == 0

    @staticmethod
    def toNativePath(path : str) -> str:
        return OsUtils.toWindowsPath(path)

    @staticmethod
    def enableAnsiColors():
        # tell Windows 10 that we do ansi
        ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-11), 7)


    @staticmethod
    def killProcess(name : str="*", prefix : str=None) -> bool:
        if not prefix:
            prefix = CraftCore.standardDirs.craftRoot()
        out = subprocess.run(f"powershell -NoProfile -ExecutionPolicy ByPass -Command \"& {{" +
                             f"Get-Process '{name}' | Where-Object {{$_.Path -like '{prefix}*'}} | Stop-Process}}\"", shell=True, stderr=subprocess.STDOUT)
        CraftCore.log.debug(f"killProcess {out.args}: {out.stdout} {out.returncode}")
        return out.returncode == 0
