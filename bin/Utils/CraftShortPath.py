import io
import os
import subprocess
import zlib
from pathlib import Path

import utils
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils


class CraftShortPath(object):
    _useShortpaths = OsUtils.isWin()
    _shortPaths = {}

    def __init__(self, path, createShortPath=None) -> None:
        self._longPath = path
        self._shortPath = None  # type: Path
        if not createShortPath:
            self._createShortPathLambda = CraftShortPath.createJunctionShortPath
        else:
            self._createShortPathLambda = createShortPath

    def path(self, condition):
        return self.shortPath if condition else self.longPath

    @property
    def longPath(self) -> str:
        return self._longPath() if callable(self._longPath) else self._longPath

    @property
    def shortPath(self) -> str:
        if self._shortPath:
            return self._shortPath
        self._shortPath = CraftShortPath._shortPaths.get(self.longPath, None)
        if not self._shortPath:
            self._shortPath = self._createShortPathLambda(self.longPath)
            CraftShortPath._shortPaths[self.longPath] = self._shortPath
        if self._shortPath != self.longPath:
            os.makedirs(self.longPath, exist_ok=True)
        return self._shortPath

    @staticmethod
    def createJunctionShortPath(longPath) -> Path:
        if not CraftShortPath._useShortpaths:
            return longPath
        import utils

        utils.createDir(CraftCore.standardDirs.junctionsDir())
        longPath = OsUtils.toNativePath(longPath)
        path = CraftCore.standardDirs.junctionsDir() / hex(zlib.crc32(bytes(str(longPath), "UTF-8")))[2:]
        delta = len(str(longPath)) - len(str(path))
        if delta <= 0:
            CraftCore.debug.log.debug(f"Using junctions for {longPath} wouldn't save characters returning original path")
            CraftCore.debug.log.debug(f"{longPath}\n" f"{path}, gain: {delta}")
            return longPath
        utils.createDir(longPath)
        if not os.path.isdir(path):
            if OsUtils.isUnix():
                ok = utils.createSymlink(longPath, path, useAbsolutePath=True, targetIsDirectory=True)
            else:
                # note: mklink is a CMD command => needs shell
                ok = utils.system(
                    ["mklink", "/J", path, longPath],
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    logCommand=False,
                )

            if not ok:
                CraftCore.debug.log.critical(f"Could not create shortpath {path}, for {longPath}")
                return longPath
        else:
            if not os.path.samefile(path, longPath):
                CraftCore.debug.log.critical(f"Existing short path {path}, did not match {longPath}")
                return longPath
        CraftCore.debug.log.debug(f"Mapped \n" f"{longPath} to\n" f"{path}, gained {delta}")
        return path

    @staticmethod
    def createSubstShortPath(longPath) -> Path:
        drive = CraftCore.settings.get("ShortPath", "DriveLetter", None)
        if not drive:
            raise Exception("Please specify a drive letter, for drive based short paths")
        # ensure we end on /
        drive = Path(drive) / "/"
        with io.StringIO() as tmp:
            if not utils.system(["subst"], stdout=tmp, logCommand=False):
                CraftCore.debug.log.critical(f"Could not create shortpath {drive}, for {longPath}. Failed to list substituted paths.")
                return longPath
            drives = dict(line.split(": =>") for line in tmp.getvalue().strip().split("\r\n"))
        if str(drive) in drives:
            if drives[str(drive)] == longPath:
                return drive
            else:
                if not utils.system(["subst", "/D", drive.drive], stdout=subprocess.DEVNULL, logCommand=False):
                    CraftCore.debug.log.critical(f"Could not create shortpath {drive}, for {longPath}. Failed to unset substituted path.")
                    return longPath
        if not utils.system(["subst", drive.drive, longPath], stdout=subprocess.DEVNULL, logCommand=False):
            CraftCore.debug.log.critical(f"Could not create shortpath {drive}, for {longPath}. Failed to substitute path.")
            return longPath
        return drive
