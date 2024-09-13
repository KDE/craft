from pathlib import Path

from CraftCore import CraftCore
from CraftOS.OsDetection import OsDetection


class Location(object):
    """
    Something like http://doc.qt.io/qt-5/qstandardpaths.html
    """

    def __init__(self, standardDirs):
        self._standardDirs = standardDirs

    @property
    def data(self) -> Path:
        if CraftCore.compiler.platform.isWindows:
            return self._standardDirs.craftRoot() / "bin/data"
        else:
            return self._standardDirs.craftRoot() / "share"


class CraftStandardDirs(object):
    _SUBST = None

    def __init__(self, craftRoot=None):
        self._craftRoot = Path(craftRoot or CraftCore.settings._craftRoot())
        self._downloadDir = Path(CraftCore.settings.get("Paths", "DOWNLOADDIR", self._craftRoot / "download"))
        self._gitDir = Path(CraftCore.settings.get("Paths", "KDEGITDIR", self._downloadDir / "git"))
        self._junctionDir = Path(CraftCore.settings.get("ShortPath", "JunctionDir", f"{self._craftRoot.drive}/_")).absolute()
        self.locations = Location(self)

    @staticmethod
    def downloadDir() -> Path:
        """location of directory where fetched files are  stored"""
        return CraftCore.standardDirs._downloadDir

    @staticmethod
    def svnDir() -> Path:
        return Path(CraftCore.settings.get("Paths", "KDESVNDIR", CraftStandardDirs.downloadDir() / "svn"))

    @staticmethod
    def gitDir() -> Path:
        return CraftCore.standardDirs._gitDir

    @staticmethod
    def tmpDir() -> Path:
        return Path(CraftCore.settings.get("Paths", "TMPDIR", CraftStandardDirs.craftRoot() / "tmp"))

    @staticmethod
    def craftRoot() -> Path:
        return CraftCore.standardDirs._craftRoot

    @staticmethod
    def craftHostRoot() -> Path:
        if CraftCore.compiler.platform.isNative:
            return CraftCore.standardDirs.craftRoot()
        return Path(CraftCore.settings.get("Paths", "HostRoot"))

    @staticmethod
    def etcDir() -> Path:
        return CraftStandardDirs.craftRoot() / "etc"

    @staticmethod
    def craftBin() -> Path:
        return Path(CraftCore.settings._craftBin())

    @staticmethod
    def craftRepositoryDir() -> Path:
        return CraftStandardDirs.craftBin().parent / "blueprints"

    @staticmethod
    def blueprintRoot() -> Path:
        return Path(
            CraftCore.settings.get(
                "Blueprints",
                "BlueprintRoot",
                CraftStandardDirs.etcBlueprintDir() / "locations",
            )
        )

    @staticmethod
    def etcBlueprintDir() -> Path:
        """the etc directory for blueprints"""
        return CraftStandardDirs.etcDir() / "blueprints"

    @staticmethod
    def msysDir() -> Path:
        if not OsDetection.isWin():
            return Path(CraftCore.settings.get("Paths", "Msys", "/"))
        else:
            return Path(CraftCore.settings.get("Paths", "Msys", CraftStandardDirs.craftRoot() / "msys"))

    @staticmethod
    def junctionsDir() -> Path:
        return CraftCore.standardDirs._junctionDir

    @staticmethod
    def logDir() -> Path:
        return CraftCore.standardDirs.craftRoot() / "logs"
