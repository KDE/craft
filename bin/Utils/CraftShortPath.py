import os
import zlib
import subprocess

from CraftCore import CraftCore
import CraftConfig
import CraftDebug
from CraftOS.osutils import OsUtils

class CraftShortPath(object):
    _useShortpaths = OsUtils.isWin()
    _shortPaths = {}

    def __init__(self, path, createShortPath=None) -> None:
        self._longPath = path
        self._shortPath = None
        if not createShortPath:
            self._createShortPathLambda = CraftShortPath._createShortPath
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
            CraftCore.debug.log.debug(f"Mapped \n"
                                f"{self.longPath} to\n"
                                f"{self._shortPath}, gained {len(self.longPath) - len(self._shortPath)}")
        return self._shortPath

    @staticmethod
    def _createShortPath(longPath) -> str:
        import utils
        longPath = OsUtils.toNativePath(longPath)
        if not CraftShortPath._useShortpaths:
            return longPath
        if not os.path.isdir(CraftCore.standardDirs.junctionsDir()):
            os.makedirs(CraftCore.standardDirs.junctionsDir())
        path = OsUtils.toNativePath(os.path.join(CraftCore.standardDirs.junctionsDir(), str(zlib.crc32(bytes(longPath, "UTF-8")))))
        if len(longPath) < len(path):
            CraftCore.debug.log.debug(f"Using junctions for {longPath} wouldn't save characters returning original path")
            CraftCore.debug.log.debug(f"{longPath}\n"
                                      f"{path}, gain:{len(longPath) - len(path)}")
            return longPath
        os.makedirs(longPath, exist_ok=True)
        if not os.path.isdir(path):
            # note: mklink is a CMD command => needs shell
            if not utils.system(["mklink", "/J", path, longPath], shell=True, stdout=subprocess.DEVNULL, logCommand=False):
                CraftCore.debug.log.critical(f"Could not create shortpath {path}, for {longPath}")
                return longPath
        else:
            if not os.path.samefile(path, longPath):
                CraftCore.debug.log.critical(f"Existing short path {path}, did not match {longPath}")
                return longPath
        return path
