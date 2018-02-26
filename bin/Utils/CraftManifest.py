import collections
import datetime
import json
import os


from CraftCore import CraftCore
import utils

class CraftManifestEntryFile(object):
    def __init__(self, fileName : str, checksum : str, version : str="") -> None:
        self.fileName = fileName
        self.checksum = checksum
        self.date = datetime.datetime.utcnow()
        self.version = version

    @staticmethod
    def fromJson(data : dict):
        out = CraftManifestEntryFile(data["fileName"], data["checksum"])
        out.date = CraftManifest._parseTimeStamp(data["date"])
        out.version = data.get("version", "")
        return out

    def toJson(self) -> dict:
        return {"fileName":self.fileName, "checksum":self.checksum, "date":self.date.strftime(CraftManifest._TIME_FORMAT), "version":self.version}

class CraftManifestEntry(object):
    def __init__(self, name : str) -> None:
        self.name = name
        self.files = []

    @staticmethod
    def fromJson(data : dict):
        entry = CraftManifestEntry(data["name"])
        entry.files = sorted([CraftManifestEntryFile.fromJson(fileData) for fileData in data["files"]], key=lambda x:x.date, reverse=True)
        return entry

    def toJson(self) -> dict:
        return {"name":self.name, "files":[x.toJson() for x in self.files]}

    def addFile(self, fileName : str, checksum : str, version : str="") -> CraftManifestEntryFile:
        f = CraftManifestEntryFile(fileName, checksum, version)
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
        out = {"date":str(self.date), "packages":{}, "version": CraftManifest.version()}
        for compiler, packages in self.packages.items():
            out["packages"][compiler] = [x.toJson() for x in self.packages[compiler].values()]
        return out

    def get(self, package : str) -> CraftManifestEntry:
        compiler = str(CraftCore.compiler)
        if not compiler in self.packages:
            self.packages[compiler] = {}
        if not package in self.packages[compiler]:
            self.packages[compiler][package] = CraftManifestEntry(package)
        return self.packages[compiler][package]

    def dump(self, cacheFilePath):
        with open(cacheFilePath, "wt+") as cacheFile:
            json.dump(self, cacheFile, sort_keys=True, indent=2, default=lambda x:x.toJson())

    @staticmethod
    def load(manifestFileName : str, urls : [str]=None):
        """
        Load a manifest.
        If a url is provided a manifest is fetch from that the url and merged with a local manifest.
        TODO: in that case we are merging all repositories so we should also merge the cache files
        """
        old = None
        if not urls and ("ContinuousIntegration", "RepositoryUrl") in CraftCore.settings and not os.path.isfile(manifestFileName):
            urls = [CraftCore.settings.get("ContinuousIntegration", "RepositoryUrl").rstrip("/")]
        if urls:
            old = CraftManifest()
            for url in urls:
                old.update(CraftManifest.fromJson(CraftCore.cache.cacheJsonFromUrl(f"{url}/manifest.json")))

        cache = None
        if os.path.isfile(manifestFileName):
            try:
                with open(manifestFileName, "rt+") as cacheFile:
                    cache = json.load(cacheFile)
            except:
                pass
            finally:
                if cache:
                    date = CraftManifest._parseTimeStamp(cache["date"])
                else:
                    date = datetime.datetime.utcnow()
                utils.copyFile(manifestFileName, manifestFileName + date.strftime("%Y%m%dT%H%M%S"))
        if old:
            if cache:
                old.update(CraftManifest.fromJson(cache))
            return old
        if not cache:
            return CraftManifest()
        return CraftManifest.fromJson(cache)

    @staticmethod
    def _parseTimeStamp(time : str) -> datetime.datetime:
        return datetime.datetime.strptime(time, CraftManifest._TIME_FORMAT)
