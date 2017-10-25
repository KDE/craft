import collections
import datetime
import json
import os


from CraftCore import CraftCore
import utils

class CraftManifestEntryFile(object):
    def __init__(self, fileName : str, checksum : str) -> None:
        self.fileName = fileName
        self.checksum = checksum
        self.date = datetime.datetime.utcnow()

    @staticmethod
    def fromJson(data : dict):
        out = CraftManifestEntryFile(data["fileName"], data["checksum"])
        out.date = datetime.datetime.strptime(data["date"], "%Y-%m-%d %H:%M:%S.%f")
        return out

    def toJson(self) -> dict:
        return {"fileName":self.fileName, "checksum":self.checksum, "date":str(self.date)}

class CraftManifestEntry(object):
    def __init__(self, name : str) -> None:
        self.name = name
        self.files = collections.OrderedDict()

    @staticmethod
    def fromJson(data : dict):
        entry = CraftManifestEntry(data["name"])
        files = sorted([CraftManifestEntryFile.fromJson(fileData) for fileData in data["files"]], key=lambda x:x.date)
        entry.files = collections.OrderedDict([(x.fileName, x) for x in files])
        return entry

    def toJson(self) -> dict:
        return {"name":self.name, "files":[x.toJson() for x in self.files.values()]}

    def addFile(self, fileName : str, checksum : str) -> CraftManifestEntryFile:
        f = CraftManifestEntryFile(fileName, checksum)
        self.files[fileName] = f
        return f

    @property
    def latest(self) -> CraftManifestEntryFile:
        return list(self.files.values())[-1]

class CraftManifest(object):
    def __init__(self):
        self.date = str(datetime.datetime.utcnow())
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
                f.date = datetime.dateime(0, 0, 0)
        return manifest

    @staticmethod
    def fromJson(data : dict):
        version = data.get("version", 0)
        if version == 0:
            return CraftManifest._migrate0(data)
        elif version != CraftManifest.version():
            raise Exception("Invalid manifest version detected")

        manifest = CraftManifest()
        manifest.date = data["date"]
        for compiler in data["packages"]:
            manifest.packages[compiler] = {}
            for package in data["packages"][compiler]:
                p = CraftManifestEntry.fromJson(package)
                manifest.packages[compiler][p.name] = p
        return manifest

    def toJson(self) -> dict:
        out = {"date":self.date, "packages":{}, "version": CraftManifest.version()}
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
    def load(manifestFileName : str):
        if ("ContinuousIntegration", "RepositoryUrl") in CraftCore.settings and not os.path.isfile(manifestFileName):
            url = CraftCore.settings.get("ContinuousIntegration", "RepositoryUrl")
            if not url.endswith("/"):
                url += "/"
            utils.getFile(f"{url}manifest.json", os.path.dirname(manifestFileName))

        if os.path.isfile(manifestFileName):
            try:
                with open(manifestFileName, "rt+") as cacheFile:
                    cache = json.load(cacheFile)
            except:
                return CraftManifest()
        else:
            return CraftManifest()

        return CraftManifest.fromJson(cache)

