import os
import platform
import subprocess

from CraftConfig import craftSettings
from CraftOS.OsDetection import OsDetection


class CraftStandardDirs(object):
    __pathCache = dict()
    __noShortPathCache = dict()
    _allowShortpaths = True
    _SUBST = None

    @staticmethod
    def _deSubstPath(path):
        """desubstitude craft short path"""

        if not OsDetection.isWin():
            return path
        drive, tail = os.path.splitdrive(path)
        drive = drive.upper()
        if CraftStandardDirs._SUBST == None:
            tmp = subprocess.getoutput("subst").split("\n")
            CraftStandardDirs._SUBST = dict()
            for s in tmp:
                if s != "":
                    key, val = s.split("\\: => ")
                    CraftStandardDirs._SUBST[key] = val
        if drive in CraftStandardDirs._SUBST:
            deSubst = CraftStandardDirs._SUBST[drive] + tail
            return deSubst
        return path

    @staticmethod
    def _pathCache():
        if CraftStandardDirs._allowShortpaths:
            return CraftStandardDirs.__pathCache
        else:
            return CraftStandardDirs.__noShortPathCache

    @staticmethod
    def allowShortpaths(allowd):
        old = CraftStandardDirs._allowShortpaths
        CraftStandardDirs._allowShortpaths = allowd
        return old

    @staticmethod
    def isShortPathEnabled():
        return platform.system() == "Windows" and CraftStandardDirs._allowShortpaths and craftSettings.getboolean(
            "ShortPath", "Enabled", False)

    @staticmethod
    def downloadDir():
        """ location of directory where fetched files are  stored """
        if not "DOWNLOADDIR" in CraftStandardDirs._pathCache():
            if CraftStandardDirs.isShortPathEnabled() and ("ShortPath", "DownloadDrive") in craftSettings:
                CraftStandardDirs._pathCache()["DOWNLOADDIR"] = CraftStandardDirs.nomalizePath(
                    craftSettings.get("ShortPath", "DownloadDrive"))
            else:
                CraftStandardDirs._pathCache()["DOWNLOADDIR"] = craftSettings.get("Paths", "DOWNLOADDIR",
                                                                                  os.path.join(
                                                                                      CraftStandardDirs.craftRoot(),
                                                                                      "download"))
        return CraftStandardDirs._pathCache()["DOWNLOADDIR"]

    @staticmethod
    def svnDir():
        if not "SVNDIR" in CraftStandardDirs._pathCache():
            CraftStandardDirs._pathCache()["SVNDIR"] = craftSettings.get("Paths", "KDESVNDIR",
                                                                         os.path.join(
                                                                             CraftStandardDirs.downloadDir(),
                                                                             "svn"))
        return CraftStandardDirs._pathCache()["SVNDIR"]

    @staticmethod
    def gitDir():
        if not "GITDIR" in CraftStandardDirs._pathCache():
            if CraftStandardDirs.isShortPathEnabled() and ("ShortPath", "GitDrive") in craftSettings:
                CraftStandardDirs._pathCache()["GITDIR"] = CraftStandardDirs.nomalizePath(
                    craftSettings.get("ShortPath", "GitDrive"))
            else:
                CraftStandardDirs._pathCache()["GITDIR"] = craftSettings.get("Paths", "KDEGITDIR",
                                                                             os.path.join(
                                                                                 CraftStandardDirs.downloadDir(),
                                                                                 "git"))
        return CraftStandardDirs._pathCache()["GITDIR"]

    @staticmethod
    def tmpDir():
        if not "TMPDIR" in CraftStandardDirs._pathCache():
            CraftStandardDirs._pathCache()["TMPDIR"] = craftSettings.get("Paths", "TMPDIR",
                                                                         os.path.join(CraftStandardDirs.craftRoot(),
                                                                                      "tmp"))
        return CraftStandardDirs._pathCache()["TMPDIR"]

    @staticmethod
    def nomalizePath(path):
        if path.endswith(":"):
            path += "\\"
        return path

    @staticmethod
    def craftRoot():
        if not "EMERGEROOT" in CraftStandardDirs._pathCache():
            if CraftStandardDirs.isShortPathEnabled() and ("ShortPath", "RootDrive") in craftSettings:
                CraftStandardDirs._pathCache()["EMERGEROOT"] = CraftStandardDirs.nomalizePath(
                    craftSettings.get("ShortPath", "RootDrive"))
            else:
                CraftStandardDirs._pathCache()["EMERGEROOT"] = craftSettings._craftRoot()
        return CraftStandardDirs._pathCache()["EMERGEROOT"]

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
        if ("Blueprints", "BlueprintRoot") in craftSettings:
            return craftSettings.get("Blueprints", "BlueprintRoot")
        return os.path.join(CraftStandardDirs.etcBlueprintDir(), "locations")

    @staticmethod
    def etcBlueprintDir():
        """the etc directory for blueprints"""
        return os.path.join(CraftStandardDirs.etcDir(), "blueprints")

    @staticmethod
    def msysDir():
        if not OsDetection.isWin():
            return craftSettings.get("Paths", "Msys", "/")
        else:
            if ("Paths", "Msys") in craftSettings:
                return craftSettings.get("Paths", "Msys")
            return os.path.join(CraftStandardDirs.craftRoot(), "msys")

    @staticmethod
    def junctionsDir(getDir=False):
        if "JunctionDir" not in CraftStandardDirs._pathCache():
            if not getDir and ("ShortPath", "JunctionDrive") in craftSettings:
                CraftStandardDirs._pathCache()["JunctionDir"] = CraftStandardDirs.nomalizePath(
                    craftSettings.get("ShortPath", "JunctionDrive"))
            else:
                path = craftSettings.get("ShortPath", "JunctionDir",
                                     os.path.join(CraftStandardDirs.craftRoot(), "build", "shortPath"))
                if not os.path.isdir(path):
                    os.makedirs(path)
                CraftStandardDirs._pathCache()["JunctionDir"] = path
                if getDir:
                    return path
        return CraftStandardDirs.__pathCache["JunctionDir"]


class TemporaryUseShortpath(object):
    """Context handler for temporarily different shortpath setting"""

    def __init__(self, enabled):
        self.prev = CraftStandardDirs.allowShortpaths(enabled)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, trback):
        CraftStandardDirs.allowShortpaths(self.prev)
