import collections
import datetime

from CraftCore import CraftCore


class CraftManifestEntryFile(object):
    def __init__(self, fileName: str, checksum: str, version: str = "") -> None:
        self.fileName = fileName
        self.checksum = checksum
        self.date = datetime.datetime.now(datetime.timezone.utc)
        self.version = version
        self.buildPrefix = str(CraftCore.standardDirs.craftRoot())
        # deprecated use config
        self.configHash = None
        self.config = None

        if CraftCore.compiler.platform.isWindows:
            self.fileName = self.fileName.replace("\\", "/")

    @staticmethod
    def fromJson(data: dict):
        out = CraftManifestEntryFile(data["fileName"], data["checksum"])
        out.date = CraftManifest._parseTimeStamp(data["date"])
        out.version = data.get("version", "")
        out.buildPrefix = data.get("buildPrefix", None)
        out.configHash = data.get("configHash", None)
        out.config = collections.OrderedDict(data.get("config", {}))
        return out

    def toJson(self) -> dict:
        data = {
            "fileName": self.fileName,
            "checksum": self.checksum,
            "date": self.date.strftime(CraftManifest._TIME_FORMAT),
            "version": self.version,
        }
        if self.config or self.configHash:
            data.update({"buildPrefix": self.buildPrefix, "config": self.config})
            if self.configHash and not self.config:
                # only keep if legacy
                data["configHash"] = self.configHash
        return data


class CraftManifestEntry(object):
    def __init__(self, name: str) -> None:
        self.name = name
        self.files = []  # type: List[CraftManifestEntryFile]

    @staticmethod
    def fromJson(data: dict):
        entry = CraftManifestEntry(data["name"])
        entry.files = sorted(
            [CraftManifestEntryFile.fromJson(fileData) for fileData in data["files"]],
            key=lambda x: x.date,
            reverse=True,
        )
        return entry

    def toJson(self) -> dict:
        return {
            "name": self.name,
            "files": [x.toJson() for x in collections.OrderedDict.fromkeys(self.files)],
        }

    def addFile(self, fileName: str, checksum: str, version: str = "", config=None) -> CraftManifestEntryFile:
        f = CraftManifestEntryFile(fileName, checksum, version)
        if config:
            f.config = config.dump()
        self.files.insert(0, f)
        return f

    @property
    def latest(self) -> CraftManifestEntryFile:
        return self.files[0] if self.files else None


class CraftManifest(object):
    _TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

    def __init__(self):
        self.date = datetime.datetime.now(datetime.timezone.utc)
        self.packages = {str(CraftCore.compiler): {}}
        self.origin = None

    @staticmethod
    def version() -> int:
        return 1

    @staticmethod
    def fromJson(data: dict):
        version = data.get("version", 0)
        if version != CraftManifest.version():
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
            if compiler not in self.packages:
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
        if compiler not in self.packages:
            self.packages[compiler] = {}
        if package not in self.packages[compiler]:
            self.packages[compiler][package] = CraftManifestEntry(package)
        return self.packages[compiler][package]

    @staticmethod
    def _parseTimeStamp(time: str) -> datetime.datetime:
        return datetime.datetime.strptime(time, CraftManifest._TIME_FORMAT)
