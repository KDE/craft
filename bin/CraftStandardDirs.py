import os
import subprocess

from CraftCore import CraftCore

import CraftConfig
from CraftOS.OsDetection import OsDetection
from Utils.CraftShortPath import CraftShortPath

class Location(object):
    """
    Something like http://doc.qt.io/qt-5/qstandardpaths.html
    """
    def __init__(self, standardDirs):
      self._standardDirs = standardDirs

    @property
    def data(self):
      if CraftCore.compiler.isWindows:
          return os.path.join(self._standardDirs.craftRoot(), "bin", "data")
      else:
          return os.path.join(self._standardDirs.craftRoot(), "share")


class CraftStandardDirs(object):
    _SUBST = None
    _allowShortpaths = True

    def __init__(self, craftRoot=None):
        self._useShortPath = False
        self._craftRoot = CraftShortPath(CraftStandardDirs._deSubstPath(craftRoot or CraftCore.settings._craftRoot()),
                                                      lambda x : CraftStandardDirs._nomalizePath(CraftCore.settings.get("ShortPath", "RootDrive", x)))
        self._downloadDir = CraftShortPath(CraftCore.settings.get("Paths", "DOWNLOADDIR",
                                                                  lambda : os.path.join( self._craftRoot.path(self.isShortPathEnabled()), "download")),
                                        lambda x : CraftStandardDirs._nomalizePath(CraftCore.settings.get("ShortPath", "DownloadDrive", x)))
        self._gitDir = CraftShortPath(CraftCore.settings.get("Paths", "KDEGITDIR",
                                                             lambda : os.path.join(self._downloadDir.path(self.isShortPathEnabled()), "git")),
                                        lambda x : CraftStandardDirs._nomalizePath(CraftCore.settings.get("ShortPath", "GitDrive", x)))
        self._junctionDir = CraftShortPath(CraftCore.settings.get("ShortPath", "JunctionDir",
                                                                  lambda : os.path.join(self._craftRoot.path(self.isShortPathEnabled()), "build", "_")),
                                        lambda x: CraftStandardDirs._nomalizePath(CraftCore.settings.get("ShortPath", "JunctionDrive", x)))

        self.locations = Location(self)

    @staticmethod
    def _deSubstPath(path):
        """desubstitude craft short path"""

        if not OsDetection.isWin():
            return path
        drive, tail = os.path.splitdrive(path)
        drive = drive.upper()
        if CraftStandardDirs._SUBST == None:
            tmp = subprocess.getoutput("subst").split("\n")
            CraftStandardDirs._SUBST = {}
            for s in tmp:
                if s != "":
                    key, val = s.split("\\: => ")
                    CraftStandardDirs._SUBST[key] = val
        if drive in CraftStandardDirs._SUBST:
            deSubst = CraftStandardDirs._SUBST[drive] + tail
            return deSubst
        return path

    @staticmethod
    def _nomalizePath(path):
        if path.endswith(":"):
            path += "\\"
        return path

    @staticmethod
    def allowShortpaths(allowd):
        old = CraftStandardDirs._allowShortpaths
        CraftStandardDirs._allowShortpaths = allowd
        return old

    @staticmethod
    def isShortPathEnabled():
        return OsDetection.isWin() and CraftStandardDirs._allowShortpaths and CraftCore.settings.getboolean(
            "ShortPath", "Enabled", False)

    @staticmethod
    def downloadDir():
        """ location of directory where fetched files are  stored """
        return CraftCore.standardDirs._downloadDir.path(CraftStandardDirs.isShortPathEnabled())

    @staticmethod
    def svnDir():
        return CraftCore.settings.get("Paths", "KDESVNDIR", os.path.join(CraftStandardDirs.downloadDir(), "svn"))

    @staticmethod
    def gitDir():
        return CraftCore.standardDirs._gitDir.path(CraftStandardDirs.isShortPathEnabled())


    @staticmethod
    def tmpDir():
        return CraftCore.settings.get("Paths", "TMPDIR",os.path.join(CraftStandardDirs.craftRoot(),"tmp"))

    @staticmethod
    def craftRoot():
        return CraftCore.standardDirs._craftRoot.path(CraftStandardDirs.isShortPathEnabled())

    @staticmethod
    def etcDir():
        return os.path.join(CraftStandardDirs.craftRoot(), "etc")

    @staticmethod
    def craftBin():
        return os.path.dirname(__file__)

    @staticmethod
    def craftRepositoryDir():
        return os.path.join(CraftStandardDirs.craftBin(), "..", "blueprints")

    @staticmethod
    def blueprintRoot():
        return CraftCore.settings.get("Blueprints", "BlueprintRoot",
                                 os.path.join(CraftStandardDirs.etcBlueprintDir(), "locations"))

    @staticmethod
    def etcBlueprintDir():
        """the etc directory for blueprints"""
        return os.path.join(CraftStandardDirs.etcDir(), "blueprints")

    @staticmethod
    def msysDir():
        if not OsDetection.isWin():
            return CraftCore.settings.get("Paths", "Msys", "/")
        else:
            return CraftCore.settings.get("Paths", "Msys",
                                     os.path.join(CraftStandardDirs.craftRoot(), "msys"))

    @staticmethod
    def junctionsDir():
        return CraftCore.standardDirs._junctionDir.path(CraftStandardDirs.isShortPathEnabled())

class TemporaryUseShortpath(object):
    """Context handler for temporarily different shortpath setting"""

    def __init__(self, enabled):
        self.prev = CraftStandardDirs.allowShortpaths(enabled)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, trback):
        CraftStandardDirs.allowShortpaths(self.prev)
