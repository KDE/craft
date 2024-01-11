import collections
import datetime
import json
import os
import shutil
from enum import Enum, auto, unique
from pathlib import Path
from typing import List

import utils
from CraftCompiler import CraftCompilerSignature
from CraftCore import CraftCore


@unique
class FileType(Enum):
    Binary = auto()
    Debug = auto()
    Source = auto()
    Logs = auto()

    @classmethod
    def fromString(cls, name):
        if not hasattr(cls, "__sting_map"):
            cls.__sting_map = dict([(k.lower(), v) for k, v in cls.__members__.items()])
        return cls.__sting_map[name.lower()]


class CraftManifestEntryFile(object):
    def __init__(self, fileType: FileType, fileName: str, checksum: str):
        self.fileType = fileType
        self.fileName = fileName
        self.checksum = checksum

    @staticmethod
    def fromJson(data: dict):
        return CraftManifestEntryFile(FileType.fromString(data["fileType"]), data["fileName"], data["checksum"])

    def toJson(self) -> dict:
        return {
            "fileName": self.fileName,
            "checksum": self.checksum,
            "fileType": self.fileType.name,
        }


class CraftManifestBuild(object):
    def __init__(self, version: str) -> None:
        self.date = datetime.datetime.now(datetime.timezone.utc)
        self.version = version
        self.buildPrefix = str(CraftCore.standardDirs.craftRoot())
        # deprecated use config
        self.configHash = None
        self.config = None

        # the revision is used for version pinning (shelves)
        self.revision = None

        self.files = {}  # Dict[FileType, CraftManifestEntryFiles]

    def addFile(self, fileType: FileType, fileName: str, checksum: str) -> CraftManifestEntryFile:
        f = CraftManifestEntryFile(fileType=fileType, fileName=fileName, checksum=checksum)
        self.files[fileType] = f
        return f

    @staticmethod
    def fromJson(data: dict):
        out = CraftManifestBuild(data.get("version", ""))
        out.date = CraftManifest._parseTimeStamp(data["date"])
        out.buildPrefix = data.get("buildPrefix", None)
        out.configHash = data.get("configHash", None)
        out.config = collections.OrderedDict(data.get("config", {}))
        out.revision = data.get("revision", None)

        for _, v in data["files"].items():
            f = CraftManifestEntryFile.fromJson(v)
            out.files[f.fileType] = f
        return out

    def toJson(self) -> dict:
        files = {}
        # map enum to name
        for k, v in self.files.items():
            files[k.name] = v
        data = {
            "files": files,
            "date": self.date.strftime(CraftManifest._TIME_FORMAT),
            "version": self.version,
        }
        if self.revision:
            data["revision"] = self.revision
        if self.config or self.configHash:
            data.update({"buildPrefix": self.buildPrefix, "config": self.config})
            if self.configHash and not self.config:
                # only keep if legacy
                data["configHash"] = self.configHash
        return data


class CraftManifestEntry(object):
    def __init__(self, name: str) -> None:
        self.name = name
        self.build = []  # type: List[CraftManifestBuild]

    @staticmethod
    def fromJson(data: dict):
        entry = CraftManifestEntry(data["name"])
        entry.build = sorted(
            [CraftManifestBuild.fromJson(fileData) for fileData in data["build"]],
            key=lambda x: x.date,
            reverse=True,
        )
        return entry

    def toJson(self) -> dict:
        return {
            "name": self.name,
            "build": [x.toJson() for x in collections.OrderedDict.fromkeys(self.build)],
        }

    def addBuild(self: str, version: str, config, revision=None) -> CraftManifestBuild:
        f = CraftManifestBuild(version)
        if config:
            f.config = config.dump()
        f.revision = revision
        self.build.insert(0, f)
        return f

    @property
    def latest(self) -> CraftManifestBuild:
        return self.build[0] if self.build else None


class CraftManifest(object):
    _TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f%z"

    def __init__(self):
        self.date = datetime.datetime.now(datetime.timezone.utc)
        self.packages = {str(CraftCore.compiler): {}}
        self.origin = None

    @staticmethod
    def version() -> int:
        return 2

    @staticmethod
    def _migrate1(data: dict):
        from Utils import CraftManifestV1

        manifest = CraftManifestV1.CraftManifest.fromJson(data)
        out = CraftManifest()
        out.origin = manifest.origin
        out.date = manifest.date
        for k, v in manifest.packages.items():
            signatue = CraftCompilerSignature.parseAbi(k)
            out.packages[str(signatue)] = {}
            for name, entry in v.items():
                out.packages[str(signatue)][name] = e = CraftManifestEntry(name)
                for f in entry.files:
                    p = e.addBuild(f.version, None)
                    p.addFile(FileType.Binary, f.fileName, f.checksum)
                    p.config = f.config
                    p.buildPrefix = f.buildPrefix
                    p.date = f.date
                # ensure sorting
                e.build = sorted(e.build, key=lambda x: x.date, reverse=True)
        return out

    @staticmethod
    def fromJson(data: dict):
        if not data:
            return CraftManifest()
        version = data.get("version", -1)
        if version == 1:
            return CraftManifest._migrate1(data)
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
        out = {
            "date": str(self.date),
            "origin": self.origin,
            "packages": {},
            "version": CraftManifest.version(),
        }
        for compiler, packages in self.packages.items():
            out["packages"][compiler] = [x.toJson() for x in self.packages[compiler].values()]
        return out

    def get(self, package: str, compiler: str = None) -> CraftManifestEntry:
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
        self.date = datetime.datetime.now(datetime.timezone.utc)
        if self.origin:
            CraftCore.log.info(f"Updating cache manifest from: {self.origin} in: {cacheFilePath}")
        else:
            CraftCore.log.info(f"Create new cache manifest: {cacheFilePath}")
        cacheFilePath.parent.mkdir(parents=True, exist_ok=True)
        with open(cacheFilePath, "wt") as cacheFile:
            json.dump(self, cacheFile, sort_keys=True, indent=2, default=lambda x: x.toJson())
        shutil.copy2(cacheFilePath, cacheFilePathTimed)

    @staticmethod
    def load(manifestFileName: str, urls: [str] = None):
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
                CraftCore.log.warning(f"Failed to load {cacheFile}", exc_info=e)
                pass
        if old:
            if cache:
                old.update(cache)
            return old
        if not cache:
            return CraftManifest()
        return cache

    @staticmethod
    def _parseTimeStamp(time: str) -> datetime.datetime:
        try:
            return datetime.datetime.strptime(time, CraftManifest._TIME_FORMAT)
        except ValueError:
            return datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f").astimezone(datetime.timezone.utc)
