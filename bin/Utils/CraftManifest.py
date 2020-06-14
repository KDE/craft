import collections
import datetime
import json
import os
import shutil
from pathlib import Path
from typing import List

from CraftCore import CraftCore
import utils


class CraftManifestEntryFile(object):
    def __init__(self, fileName : str, checksum : str, version : str="") -> None:
        self.fileName = fileName
        self.checksum = checksum
        self.date = datetime.datetime.utcnow()
        self.version = version
        self.buildPrefix = CraftCore.standardDirs.craftRoot()
        self.configHash = None

        if CraftCore.compiler.isWindows:
            self.fileName = self.fileName.replace("\\", "/")


    @staticmethod
    def fromJson(data : dict):
        out = CraftManifestEntryFile(data["fileName"], data["checksum"])
        out.date = CraftManifest._parseTimeStamp(data["date"])
        out.version = data.get("version", "")
        out.buildPrefix = data.get("buildPrefix", None)
        out.configHash = data.get("configHash", None)
        return out

    def toJson(self) -> dict:
        data = {
            "fileName"      : self.fileName,
            "checksum"      : self.checksum,
            "date"          : self.date.strftime(CraftManifest._TIME_FORMAT),
            "version"       : self.version
        }
        if self.configHash:
            data.update({
                "buildPrefix"   : self.buildPrefix,
                "configHash"    : self.configHash
            })
        return data

class CraftManifestEntry(object):
    def __init__(self, name : str) -> None:
        self.name = name
        self.files = [] # type: List[CraftManifestEntryFile]

    @staticmethod
    def fromJson(data : dict):
        entry = CraftManifestEntry(data["name"])
        entry.files = sorted([CraftManifestEntryFile.fromJson(fileData) for fileData in data["files"]], key=lambda x:x.date, reverse=True)
        return entry

    def toJson(self) -> dict:
        return {"name":self.name, "files": [x.toJson() for x in collections.OrderedDict.fromkeys(self.files)]}

    def addFile(self, fileName : str, checksum : str, version : str="", config=None) -> CraftManifestEntryFile:
        f = CraftManifestEntryFile(fileName, checksum, version)
        if config:
           f.configHash = config.configHash()
        self.files.insert(0, f)
        return f

    @property
    def latest(self) -> CraftManifestEntryFile:
        return self.files[0] if self.files else None

class CraftManifest(object):
    _TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

    def __init__(self):
        self.date = datetime.datetime.utcnow()
        self.packages = {str(CraftCore.compiler) : {}}
        self.origin = None

    @staticmethod
    def version() -> int:
        return 1

    @staticmethod
    def _migrate0(data : dict):
        manifest = CraftManifest()
        packages = manifest.packages[str(CraftCore.compiler)]
        for name, package in data.items():
            if not name in packages:
                packages[name] = CraftManifestEntry(name)
            p = packages[name]
            for fileName, pData in data[name].items():
                f = p.addFile(fileName, pData["checksum"])
                f.date = datetime.datetime(1, 1, 1)
        return manifest

    @staticmethod
    def fromJson(data : dict):
        version = data.get("version", 0)
        if version == 0:
            return CraftManifest._migrate0(data)
        elif version != CraftManifest.version():
            raise Exception("Invalid manifest version detected")

        manifest = CraftManifest()
        manifest.date = CraftManifest._parseTimeStamp(data["date"])
        manifest.origin = data.get("origin", None)
        for compiler in data["packages"]:
            manifest.packages[compiler] = {}
            for package in data["packages"][compiler]:
                p = CraftManifestEntry.fromJson(package)
                manifest.packages[compiler][p.name] = p
        return manifest

    def update(self, other):
        for compiler in other.packages.keys():
            if not compiler in self.packages:
                self.packages[compiler] = {}
            self.packages[compiler].update(other.packages[compiler])

    def toJson(self) -> dict:
        out = {"date": str(self.date), "origin": self.origin, "packages":{}, "version": CraftManifest.version()}
        for compiler, packages in self.packages.items():
            out["packages"][compiler] = [x.toJson() for x in self.packages[compiler].values()]
        return out

    def get(self, package : str, compiler : str=None) -> CraftManifestEntry:
        if not compiler:
            compiler = str(CraftCore.compiler)
        if not compiler in self.packages:
            self.packages[compiler] = {}
        if not package in self.packages[compiler]:
            self.packages[compiler][package] = CraftManifestEntry(package)
        return self.packages[compiler][package]

    def dump(self, cacheFilePath):
        cacheFilePath = Path(cacheFilePath)
        cacheFilePathTimed = cacheFilePath.parent / f"{cacheFilePath.stem}-{self.date.strftime('%Y%m%dT%H%M%S')}{cacheFilePath.suffix}"
        self.date = datetime.datetime.utcnow()
        if self.origin:
            CraftCore.log.info(f"Updating cache manifest from: {self.origin} in: {cacheFilePath}")
        else:
            CraftCore.log.info(f"Create new cache manifest: {cacheFilePath}")
        cacheFilePath.parent.mkdir(parents=True, exist_ok=True)
        with open(cacheFilePath, "wt") as cacheFile:
            json.dump(self, cacheFile, sort_keys=True, indent=2, default=lambda x:x.toJson())
        shutil.copy2(cacheFilePath, cacheFilePathTimed)

    @staticmethod
    def load(manifestFileName : str, urls : [str]=None):
        """
        Load a manifest.
        If a url is provided a manifest is fetch from that the url and merged with a local manifest.
        TODO: in that case we are merging all repositories so we should also merge the cache files
        """
        old = None
        if not urls and ("ContinuousIntegration", "RepositoryUrl") in CraftCore.settings:
            urls = [CraftCore.settings.get("ContinuousIntegration", "RepositoryUrl").rstrip("/")]
        if urls:
            old = CraftManifest()
            for url in urls:
                new = CraftManifest.fromJson(CraftCore.cache.cacheJsonFromUrl(utils.urljoin(url, "manifest.json")))
                if new:
                    new.origin = url
                    old.update(new)

        cache = None
        if os.path.isfile(manifestFileName):
            try:
                with open(manifestFileName, "rt") as cacheFile:
                    cache = CraftManifest.fromJson(json.load(cacheFile))
            except Exception as e:
                CraftCore.log.warning(f"Failed to load {cacheFile}, {e}")
                pass
        if old:
            if cache:
                old.update(cache)
            return old
        if not cache:
            return CraftManifest()
        return cache

    @staticmethod
    def _parseTimeStamp(time : str) -> datetime.datetime:
        return datetime.datetime.strptime(time, CraftManifest._TIME_FORMAT)
