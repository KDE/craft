from typing import Dict

import os

import CraftHash
import utils
from CraftConfig import craftSettings, CraftStandardDirs
from CraftDebug import craftDebug


class CraftShortPath(object):
    _useShortpaths = utils.OsUtils.isWin() and craftSettings.getboolean("ShortPath", "EnableJunctions", False)
    _shortPaths = {}

    def __init__(self, path) -> None:
        self.longPath = path
        self._shortPath = None


    @property
    def shortPath(self) -> str:
        if not CraftShortPath._useShortpaths:
            return self.longPath
        if not self._shortPath:
            self._shortPath = CraftShortPath._shortPaths.get(self.longPath, None)
            if not self._shortPath:
                self._shortPath = CraftShortPath._createShortPath(self.longPath)
                CraftShortPath._shortPaths[self.longPath] = self._shortPath
        craftDebug.log.info(f"Mapped \n"
                            f"{self.longPath} to\n"
                            f"{self._shortPath}, gained {len(self.longPath) - len(self._shortPath)}")
        return self._shortPath

    @staticmethod
    def _createShortPath(longPath) -> str:
        if not os.path.isdir(CraftStandardDirs.junctionsDir()):
            os.makedirs(CraftStandardDirs.junctionsDir())
        path = os.path.join(CraftStandardDirs.junctionsDir(), CraftHash.digestString(longPath, CraftHash.HashAlgorithm.MD5))
        if len(longPath) < len(path):
            craftDebug.log.info(f"Using junctions for {longPath} wouldn't save characters returning original path")
            return longPath
        if not os.path.isdir(path):
            if not os.path.isdir(longPath):
                os.makedirs(longPath)
            if not utils.system(["mklink", "/J", path, longPath]):
                craftDebug.log.critical(f"Could not create shortpath {path}, for {longPath}")
                return longPath
        else:
            if not os.path.samefile(path, longPath):
                craftDebug.log.critical(f"Existing short path {path}, did not match {longPath}")
                return longPath
        return path
