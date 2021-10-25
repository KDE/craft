import tempfile
import ctypes
import os
import platform
import subprocess
from pathlib import Path
import uuid

import CraftOS.OsUtilsBase
from CraftCore import CraftCore


class FileAttributes():
    # https://msdn.microsoft.com/en-us/library/windows/desktop/gg258117(v=vs.85).aspx
    FILE_ATTRIBUTE_READONLY = 0x1
    FILE_ATTRIBUTE_REPARSE_POINT = 0x400
    FILE_ATTRIBUTE_NORMAL = 0x80


class OsUtils(CraftOS.OsUtilsBase.OsUtilsBase):
    InDocker = None
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
                    msg += str(error)
                CraftCore.log.error(msg)
                if error == 5:
                    tmp = f"{path}-{uuid.uuid1().hex}.craft_delete"
                    MOVEFILE_DELAY_UNTIL_REBOOT = 0x4
                    MOVEFILE_WRITE_THROUGH = 0x8
                    ret = ctypes.windll.kernel32.MoveFileExW(str(path), tmp, MOVEFILE_WRITE_THROUGH)
                    error = ctypes.windll.kernel32.GetLastError()
                    CraftCore.log.error(f"MoveFileExW1 {error}")
                    ret = ctypes.windll.kernel32.MoveFileExW(tmp, 0, MOVEFILE_DELAY_UNTIL_REBOOT)
                    if not ret:
                        error = ctypes.windll.kernel32.GetLastError()
                        CraftCore.log.error(f"MoveFileExW {error}")
                        return False
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
        import shells
        if not prefix:
            prefix = CraftCore.standardDirs.craftRoot()
        prefix = Path(prefix)
        CraftCore.log.info(f"Killing processes {name} in {prefix}")
        return shells.Powershell().execute([f"Get-Process '{name}' | Where-Object {{$_.Path -like '{prefix}*'}} |"
                             f" %{{ Write-Output ('\tKilling: {{0}}' -f $_.Path); Stop-Process -Force $_;}}"], logCommand=False)

    @staticmethod
    def detectDocker():
        if OsUtils.InDocker is None:
            import shells
            OsUtils.InDocker = shells.Powershell().execute(["Get-Service", "-Name", "cexecsvc", "-ErrorAction", "SilentlyContinue"], logCommand=False)
        return OsUtils.InDocker