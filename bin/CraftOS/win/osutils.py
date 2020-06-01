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
    FILE_ATTRIBUTE_NORMAL = 0x80


class OsUtils(CraftOS.OsUtilsBase.OsUtilsBase):
    @staticmethod
    def rm(path, force=False):
        CraftCore.log.debug("deleting file %s" % path)
        if OsUtils.isLink(path):
            try:
                os.remove(path)
                return True
            except:
                return False
        try:
            os.remove(path)
        except:
            if force:
                OsUtils.setWritable(path)
            ret = ctypes.windll.kernel32.DeleteFileW(str(path)) != 0
            if not ret:
                msg = f"Deleting {path} failed error: "
                error = ctypes.windll.kernel32.GetLastError()
                if error == 5:
                    msg += "ERROR_ACCESS_DENIED"
                else:
                    msg += error
                CraftCore.log.error(msg)
                return False
        return True

    @staticmethod
    def rmDir(path, force=False):
        path = os.path.normpath(path)
        CraftCore.log.debug(f"deleting directory {path}")
        if OsUtils.isLink(path):
            return OsUtils.rm(path, force)
        if force:
            OsUtils.setWritable(path)
        with os.scandir(path) as scan:
            for f in scan:
                if f.is_dir() and not OsUtils.isLink(f.path):
                    if not OsUtils.rmDir(f.path, force):
                        return False
                else:
                    if not OsUtils.rm(f.path, force):
                        return False
        try:
            os.rmdir(path)
        except:
            return False
        return True

    @staticmethod
    def isLink(path):
        return os.path.islink(path) \
               | OsUtils.getFileAttributes(str(path)) & FileAttributes.FILE_ATTRIBUTE_REPARSE_POINT  # Detect a Junction

    @staticmethod
    def getFileAttributes(path):
        return ctypes.windll.kernel32.GetFileAttributesW(str(path))

    @staticmethod
    def removeReadOnlyAttribute(path):
        CraftCore.log.debug(f"Remove readonly flag of {path}")
        attributes = OsUtils.getFileAttributes(path)
        return ctypes.windll.kernel32.SetFileAttributesW(str(path),
                                                         attributes & ~ FileAttributes.FILE_ATTRIBUTE_READONLY) != 0

    @staticmethod
    def setWritable(path):
        return ctypes.windll.kernel32.SetFileAttributesW(str(path), FileAttributes.FILE_ATTRIBUTE_NORMAL) != 0

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
    def killProcess(name : str="*", prefix : str=None) -> bool:
        import utils
        if not prefix:
            prefix = CraftCore.standardDirs.craftRoot()
        powershell = None
        if platform.architecture()[0] == "32bit":
            # try to find the x64 powershell to be able to kill x64 processes too
            powershell = CraftCore.cache.findApplication("powershell", os.path.join(os.environ["WINDIR"], "sysnative", "WindowsPowerShell", "v1.0" ))
        if not powershell:
            powershell = CraftCore.cache.findApplication("powershell")
        if not powershell:
            CraftCore.log.warning("Failed to detect powershell")
            return False
        CraftCore.log.info(f"Killing processes {name} in {prefix}")
        return utils.system(f"{powershell} -NoProfile -ExecutionPolicy ByPass -Command \"& {{" +
                             f"Get-Process '{name}' | Where-Object {{$_.Path -like '{prefix}*'}} |"
                             f" %{{ Write-Output ('\tKilling: {{0}}' -f $_.Path); Stop-Process -Force $_;}} }}\"", logCommand=False)
