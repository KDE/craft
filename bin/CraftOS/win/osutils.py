import ctypes
import os
import shutil
import sys
import tempfile
import uuid
from enum import IntFlag
from pathlib import Path
from typing import Optional

import CraftOS.OsUtilsBase
from CraftCore import CraftCore


class FileAttributes(IntFlag):
    # https://msdn.microsoft.com/en-us/library/windows/desktop/gg258117(v=vs.85).aspx
    FILE_ATTRIBUTE_READONLY = 0x1
    FILE_ATTRIBUTE_REPARSE_POINT = 0x400
    FILE_ATTRIBUTE_NORMAL = 0x80


class MoveFlags(IntFlag):
    MOVEFILE_DELAY_UNTIL_REBOOT = 0x4


class OsUtils(CraftOS.OsUtilsBase.OsUtilsBase):
    InDocker = None

    @staticmethod
    def rm(path, force=False):
        path = Path(path)
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
            if ctypes.windll.kernel32.DeleteFileW(str(path)) == 0:
                error = ctypes.windll.kernel32.GetLastError()
                if error == 5:
                    if path.suffix != ".craft_autoremove":
                        autoRemoveName = f"{path}.{uuid.uuid4()}.craft_autoremove"
                        if shutil.move(path, autoRemoveName):
                            return False
                        CraftCore.log.debug(f"Register {autoRemoveName} for removal on restart")
                        if ctypes.windll.kernel32.MoveFileExW(autoRemoveName, None, MoveFlags.MOVEFILE_DELAY_UNTIL_REBOOT):
                            CraftCore.log.error(f"Registering {autoRemoveName} for removal on restart failed error: {ctypes.windll.kernel32.GetLastError()}")
                            return False
                else:
                    CraftCore.log.error(f"Deleting {path} failed error: {error}")
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
        return os.path.islink(path) | OsUtils.getFileAttributes(str(path)) & FileAttributes.FILE_ATTRIBUTE_REPARSE_POINT  # Detect a Junction

    @staticmethod
    def getFileAttributes(path):
        return ctypes.windll.kernel32.GetFileAttributesW(str(path))

    @staticmethod
    def removeReadOnlyAttribute(path):
        CraftCore.log.debug(f"Remove readonly flag of {path}")
        attributes = OsUtils.getFileAttributes(path)
        return ctypes.windll.kernel32.SetFileAttributesW(str(path), attributes & ~FileAttributes.FILE_ATTRIBUTE_READONLY) != 0

    @staticmethod
    def setWritable(path):
        return ctypes.windll.kernel32.SetFileAttributesW(str(path), FileAttributes.FILE_ATTRIBUTE_NORMAL) != 0

    @staticmethod
    def setConsoleTitle(title):
        return ctypes.windll.kernel32.SetConsoleTitleW(title) != 0

    @staticmethod
    def supportsSymlinks():
        with tempfile.TemporaryDirectory() as tmp:
            testFileSource = Path(tmp) / "CRAFT_LINK_TEST_SOURCE"
            with testFileSource.open("wt") as out:
                out.write("Hello from craft")
            testFileDest = Path(tmp) / "CRAFT_LINK_TEST_DEST"
            return (
                CraftCore.cache.getCommandOutput(
                    "cmd",
                    f"/C mklink {testFileDest} {testFileSource}",
                    testName="CRAFT_LINK_TEST",
                )[0]
                == 0
            )

    @staticmethod
    def toNativePath(path: str) -> str:
        return str(OsUtils.toWindowsPath(path))

    @staticmethod
    def killProcess(name: str = "*", prefix: Optional[str] = None) -> bool:
        import shells

        if not prefix:
            _prefix = CraftCore.standardDirs.craftRoot()
        prefixPath = Path(_prefix)
        CraftCore.log.info(f"Killing processes {name} in {prefixPath}")
        return shells.Powershell().execute(
            [
                f"Get-Process '{name}' | Where-Object {{$_.Path -and [IO.Path]::GetFullPath($_.Path) -like '{prefixPath.absolute()}*' -and -not ([IO.Path]::GetFullPath($_.Path) -like '{Path(sys.executable).absolute()}')}} |"
                f" %{{ Write-Output ('\tKilling: {{0}}' -f $_.Path); Stop-Process -Force $_;}}"
            ],
            logCommand=False,
        )

    @staticmethod
    def detectDocker():
        if OsUtils.InDocker is None:
            import shells

            OsUtils.InDocker = shells.Powershell().execute(
                [
                    "Get-Service",
                    "-Name",
                    "cexecsvc",
                    "-ErrorAction",
                    "SilentlyContinue",
                ],
                logCommand=False,
            )
        return OsUtils.InDocker
