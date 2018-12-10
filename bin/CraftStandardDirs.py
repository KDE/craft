import os
import subprocess

from CraftCore import CraftCore

import CraftConfig
from CraftOS.OsDetection import OsDetection

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

    def __init__(self, craftRoot=None):
        self._craftRoot = craftRoot or CraftCore.settings._craftRoot()
        self._downloadDir = CraftCore.settings.get("Paths", "DOWNLOADDIR", os.path.join(self._craftRoot, "download"))
        self._gitDir = CraftCore.settings.get("Paths", "KDEGITDIR", os.path.join( self._downloadDir, "git"))
        self._junctionDir = CraftCore.settings.get("ShortPath", "JunctionDir", os.path.join(self._craftRoot, "build", "_"))
        self.locations = Location(self)

    @staticmethod
    def _nomalizePath(path):
        if path.endswith(":"):
            path += "\\"
        return path

    @staticmethod
    def downloadDir():
        """ location of directory where fetched files are  stored """
        return CraftCore.standardDirs._downloadDir

    @staticmethod
    def svnDir():
        return CraftCore.settings.get("Paths", "KDESVNDIR", os.path.join(CraftStandardDirs.downloadDir(), "svn"))

    @staticmethod
    def gitDir():
        return CraftCore.standardDirs._gitDir


    @staticmethod
    def tmpDir():
        return CraftCore.settings.get("Paths", "TMPDIR",os.path.join(CraftStandardDirs.craftRoot(),"tmp"))

    @staticmethod
    def craftRoot():
        return CraftCore.standardDirs._craftRoot

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
        return CraftCore.standardDirs._junctionDir
