import atexit
import json
import os
import pickle
import re
import shutil
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
import sys
from pathlib import Path

from CraftCore import CraftCore, AutoImport

from Blueprints.CraftVersion import CraftVersion
from CraftOS.unix.osutils import OsUtils
from CraftStandardDirs import CraftStandardDirs
from Utils import GetFiles

class CraftCache(object):
    RE_TYPE = re.Pattern if sys.version_info >= (3,7) else re._pattern_type
    _version = 9
    _cacheLifetime = (60 * 60 * 24) * 1  # days

    class NonPersistentCache(object):
        def __init__(self):
            self.applicationLocations = {}

    def __init__(self):
        self.version = CraftCache._version
        self.cacheCreationTime = time.time()

        self._outputCache = {}
        self._helpCache = {}
        self._versionCache = {}
        self._nightlyVersions = {}
        self._jsonCache = {}
        # defined in blueprintSearch
        self.availablePackages = None

        # non persistent cache
        self._nonPersistentCache = CraftCache.NonPersistentCache()

    def __getstate__(self):
        state = dict(self.__dict__)
        del state["_nonPersistentCache"]
        return state

    def __setstate__(self, state):
        self.__dict__ = state
        self._nonPersistentCache = CraftCache.NonPersistentCache()

    @staticmethod
    def _loadInstance():
        utilsCache = CraftCache()
        if os.path.exists(CraftCache._cacheFile()):
            with open(CraftCache._cacheFile(), "rb") as f:
                try:
                    data = pickle.load(f)
                except Exception as e:
                    CraftCore.log.warning(f"Cache corrupted: {e}")
                    return utilsCache

            if data.version != CraftCache._version or (
                time.time() - data.cacheCreationTime) > CraftCache._cacheLifetime:
                CraftCore.log.debug("Clear cache")
            else:
                utilsCache = data
        return utilsCache

    @staticmethod
    def _cacheFile():
        return os.path.join(CraftStandardDirs.etcDir(), "cache.pickle")

    @staticmethod
    @atexit.register
    def _save():
        try:
            if not os.path.isdir(os.path.dirname(CraftCache._cacheFile())):
                return
            if isinstance(CraftCore.cache, AutoImport):
                return
            with open(CraftCache._cacheFile(), "wb") as f:
                pick = pickle.Pickler(f, protocol=pickle.HIGHEST_PROTOCOL)
                pick.dump(CraftCore.cache)
        except Exception as e:
            CraftCore.log.warning(f"Failed to save cache {e}", exc_info=e, stack_info=True)
            os.remove(CraftCache._cacheFile())

    def clear(self):
        CraftCore.log.debug("Clear utils cache")
        CraftCore.cache = CraftCache()

    def findApplication(self, app, path=None) -> str:
        if app in self._nonPersistentCache.applicationLocations:
            appLocation = self._nonPersistentCache.applicationLocations[app]
            if os.path.exists(appLocation):
                return appLocation
            else:
                self._helpCache.clear()

        # don't look in the build dir etc
        _cwd = os.getcwd()
        os.chdir(CraftCore.standardDirs.craftRoot())
        appLocation = shutil.which(app, path=path)
        os.chdir(_cwd)

        if appLocation:
            if OsUtils.isWin():
                # prettify command
                path, ext = os.path.splitext(appLocation)
                appLocation = path + ext.lower()
            if Path(CraftCore.standardDirs.craftRoot()) in Path(appLocation).parents:
                CraftCore.log.debug(f"Adding {app} to app cache {appLocation}")
                self._nonPersistentCache.applicationLocations[app] = appLocation
        else:
            CraftCore.log.debug(f"Craft was unable to locate: {app}, in {path}")
            return None
        return appLocation

    def getCommandOutput(self, app:str, command:str, testName:str=None) -> (int, str):
        if not testName:
            testName = f"\"{app}\" {command}"
        app = self.findApplication(app)
        if not app:
            return (-1, None)
        if testName not in self._outputCache:
            CraftCore.log.debug(f"\"{app}\" {command}")
            # TODO: port away from shell=True
            completeProcess = subprocess.run(f"\"{app}\" {command}",
                                             shell=True,
                                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                             universal_newlines=True, errors="backslashreplace")
            CraftCore.log.debug(f"{testName} Result: ExitedCode: {completeProcess.returncode} Output: {completeProcess.stdout}")
            self._outputCache[testName] = (completeProcess.returncode, completeProcess.stdout)
        return self._outputCache[testName]

    # TODO: rename, cleanup
    def checkCommandOutputFor(self, app, command, helpCommand="-h") -> str:
        if not (app, command) in self._helpCache:
            _, output = self.getCommandOutput(app, helpCommand)
            if not output:
                return False
            if type(command) == str:
                supports = command in output
            else:
                supports = command.match(output) is not None
            self._helpCache[(app, command)] = supports
            CraftCore.log.debug("%s %s %s" % (app, "supports" if supports else "does not support", command))
        return self._helpCache[(app, command)]

    def getVersion(self, app, pattern=None, versionCommand=None) -> CraftVersion:
        app = self.findApplication(app)
        if not app:
            return None
        if app in self._versionCache:
            return self._versionCache[app]
        if not pattern:
            pattern = re.compile(r"(\d+\.\d+(?:\.\d+)?)")
        if not versionCommand:
            versionCommand = "--version"
        if not isinstance(pattern, CraftCache.RE_TYPE):
            raise Exception("getVersion can only handle a compiled regular expression as pattern")
        _, output = self.getCommandOutput(app, versionCommand)
        if not output:
            return None
        match = pattern.search(output)
        if not match:
            CraftCore.log.warning(f"Could not detect pattern: {pattern.pattern} in {output}")
            return None
        appVersion = CraftVersion(match.group(1))
        self._versionCache[app] = appVersion
        CraftCore.log.debug(f"getVersion: {app}[{appVersion}]")
        return appVersion

    def cacheJsonFromUrl(self, url, timeout=10) -> object:
        CraftCore.log.debug(f"Fetch Json: {url}")
        if not url in self._jsonCache:
            if os.path.isfile(url):
                with open(url, "rt", encoding="UTF-8") as jsonFile:
                    # don't cache local manifest
                    return json.loads(jsonFile.read())
            else:
                with tempfile.TemporaryDirectory() as tmp:
                    if not GetFiles.getFile(url, tmp, "manifest.json", quiet=True):
                        # TODO: provide the error code and only cache 404...
                        self._jsonCache[url] = {}
                        return {}
                    with open(os.path.join(tmp, "manifest.json"), "rt", encoding="UTF-8") as jsonFile:
                        self._jsonCache[url] = json.loads(jsonFile.read())
        return self._jsonCache.get(url, {})

    def getNightlyVersionsFromUrl(self, url, pattern, timeout=10) -> [str]:
        """
        Returns a list of possible version number matching the regular expression in pattern.
        :param url: The url to look for the nightly builds.
        :param pattern: A regular expression to match the version.
        :param timeout:
        :return: A list of matching strings or [None]
        """
        if url not in self._nightlyVersions:
            if CraftCore.settings.getboolean("General", "WorkOffline"):
                CraftCore.debug.step("Nightly builds unavailable for %s in offline mode." % url)
                return []
            try:
                with urllib.request.urlopen(url, timeout=timeout) as fh:
                    data = str(fh.read(), "UTF-8")
                    vers = re.findall(pattern, data)
                    if not vers:
                        print(data)
                        raise Exception("Pattern %s does not match." % pattern)
                    out = list(set(vers))
                    self._nightlyVersions[url] = out
                    CraftCore.log.debug(f"Found nightlies for {url}: {out}")
                    return out
            except Exception as e:
                CraftCore.log.warning("Nightly builds unavailable for %s: %s" % (url, e))
        return self._nightlyVersions.get(url, [])
