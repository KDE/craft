import datetime
import json
import os

from CraftCore import CraftCore
import utils

class CraftManifestEntryFile(object):
    def __init__(self, fileName : str, checksum : str, date=None) -> None:
        self.fileName = fileName
        self.checksum = checksum
        self.date = date or str(datetime.datetime.utcnow())

    def toJson(self) -> dict:
        return self.__dict__

class CraftManifestEntry(object):
    def __init__(self, name : str) -> None:
        self.name = name
        self.files = {}
        self.appveyorBuildVersion = os.environ.get("APPVEYOR_BUILD_VERSION", None)

    @staticmethod
    def fromJson(data : dict):
        entry = CraftManifestEntry(data["name"])
        entry.appveyorBuildVersion = data["appveyorBuildVersion"]
        for files in data["files"]:
            f = entry.addFile(files["fileName"], files["checksum"])
            f.date = files["date"]
        return entry

    def toJson(self) -> dict:
        return {"name":self.name, "appveyorBuildVersion": self.appveyorBuildVersion, "files":[x.toJson() for x in self.files.values()]}

    def addFile(self, fileName : str, checksum : str) -> CraftManifestEntryFile:
        f = CraftManifestEntryFile(fileName, checksum)
        self.files[fileName] = f
        return f

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
                f.date = None
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
            utils.getFile(f"{url}manifest.json", os.path.basedir(manifestFileName))

        if os.path.isfile(manifestFileName):
            try:
                with open(manifestFileName, "rt+") as cacheFile:
                    cache = json.load(cacheFile)
            except:
                return CraftManifest()
        else:
            return CraftManifest()

        return CraftManifest.fromJson(cache)

