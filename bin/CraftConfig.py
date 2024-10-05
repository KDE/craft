# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2014 Hannah von Reth <vonreth@kde.org>

# central instance for managing settings regarding craft

import atexit
import configparser
import os
import sys
from pathlib import Path

from CraftCore import CraftCore


class CraftConfig(object):
    __CraftBin = None

    def __init__(self, iniPath=None):
        self._config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        if iniPath:
            self.iniPath = Path(iniPath)
        else:
            self.iniPath = CraftConfig._craftRoot() / "etc/CraftSettings.ini"
        if not self.iniPath.exists() and "CRAFT_TEST" in os.environ:
            # this should only happen when running test outside of a craft setup (eg. CI)
            self.iniPath = CraftConfig._craftBin() / "../CraftSettings.ini.template"

        self._alias = {}
        self._groupAlias = {}
        self._readSettings()

        if str(self.iniPath).endswith("CraftSettings.ini.template") and "CRAFT_TEST_ABI" in os.environ:
            # this should only happen when running test outside of a craft setup (eg. CI)
            self.set("General", "ABI", os.environ["CRAFT_TEST_ABI"])

        if self.version < 4:
            print(
                "Your configuration is outdated and no longer supported, please reinstall Craft.",
                file=sys.stderr,
            )
            exit(-1)

        if self.version < 5:
            self._setAliasesV4()

        if self.version < 6:
            self._setAliasesV5()

        if self.version < 7:
            self._setAliasesV6()

        self._warned = set()

    @staticmethod
    def _craftBin():
        if CraftConfig.__CraftBin:
            return CraftConfig.__CraftBin
        # try to locate the full path even if the craft dir is a symlink
        if "craftRoot" in os.environ:
            dir = os.environ["craftRoot"]
        else:
            dir = os.path.abspath(os.path.dirname(sys.argv[0]))
        # TODO: was there a reason to look for craaftenv.ps1 and not just for craft.py
        while dir.count(os.path.sep) > 1 and not os.path.isfile(os.path.join(dir, "craftenv.ps1")):
            dir = os.path.dirname(dir)
        if not os.path.join(dir, "craftenv.ps1"):
            print("Failed to find the craft root", file=sys.stderr)
            exit(-1)
        CraftConfig.__CraftBin = Path(os.path.join(dir, "bin"))
        return CraftConfig.__CraftBin

    @staticmethod
    def _craftRoot():
        return Path(os.path.abspath(os.path.join(CraftConfig._craftBin(), "..", "..")))

    def _setAliasesV6(self):
        self.addAlias("CodeSigning", "CommonName", "CodeSigning", "SubjectName")

    def _setAliasesV5(self):
        self.addAlias("Packager", "Destination", "General", "EMERGE_PKGDSTDIR")

    def _setAliasesV4(self):
        self.addGroupAlias("Blueprints", "Portage")
        self.addGroupAlias("BlueprintVersions", "PortageVersions")
        self.addAlias("Blueprints", "Locations", "General", "Portages")

    def _warnDeprecated(self, deprecatedSection, deprecatedKey, section, key):
        if not (deprecatedSection, deprecatedKey) in self._warned:
            self._warned.add((deprecatedSection, deprecatedKey))
            print(
                f"Warning: {deprecatedSection}/{deprecatedKey} is deprecated and has been renamed to " f"{section}/{key}, please update your CraftSettings.ini",
                file=sys.stderr if not CraftCore.settings.getboolean("ContinuousIntegration", "Enabled", False) else sys.stdout,
            )

    def _readSettings(self):
        if not os.path.exists(self.iniPath):
            print("Could not find config: %s" % self.iniPath, file=sys.stderr)
            return

        craftDir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        # read defaults
        self._config.read(os.path.join(craftDir, "etc", "CraftCoreSettings.ini"), encoding="utf-8")
        #####
        if "Variables" not in self._config.sections():
            self._config.add_section("Variables")
        for key, value in {
            "CraftRoot": CraftConfig._craftRoot(),
            "CraftDir": craftDir,
        }.items():
            self._config["Variables"][key] = str(value)
        # read user settings
        self._config.read(self.iniPath, encoding="utf-8")

    def __contains__(self, key):
        return (
            self.__contains_no_alias(key)
            or (key in self._alias and self.__contains__(self._alias[key]))
            or (key[0] in self._groupAlias and self.__contains__((self._groupAlias[key[0]], key[1])))
        )

    def __contains_no_alias(self, key):
        return self._config and self._config.has_section(key[0]) and key[1] in self._config[key[0]]

    @property
    def version(self):
        return int(self.get("Version", "ConfigVersion", 2))

    def addAlias(self, group, key, destGroup, destKey):
        self._alias[(group, key)] = (destGroup, destKey)

    def addGroupAlias(self, group, destGroup):
        self._groupAlias[group] = destGroup

    def get(self, group, key, default=None):
        if (group, key) in self._alias:
            dg, dk = self._alias[(group, key)]
            if (dg, dk) in self:
                self._warnDeprecated(dg, dk, group, key)
                return self.get(dg, dk, default)

        if group in self._groupAlias:
            oldGroup = self._groupAlias[group]
            if oldGroup in self._config.sections():
                if (oldGroup, key) in self:
                    self._warnDeprecated(oldGroup, key, group, key)
                    return self.get(oldGroup, key)

        if self.__contains_no_alias((group, key)):
            return self._config[group][key]

        if default is not None:
            return default
        print("Failed to find")
        print("\t[%s]" % group)
        print("\t%s = ..." % key)
        print("in your CraftSettings.ini")
        exit(1)

    @staticmethod
    def _parseList(s: str) -> list[str]:
        return [v.strip() for v in s.split(";") if v]

    def getList(self, group, key, default=None):
        return CraftConfig._parseList(self.get(group, key, default))

    def getSection(self, group):
        if self._config.has_section(group):
            return self._config.items(group)
        else:
            return []

    def getboolean(self, group, key, default=False):
        val = self.get(group, key, str(default))
        return self._config._convert_to_boolean(val)

    def set(self, group, key, value):
        if value is None:
            return
        if not self._config.has_section(group):
            self._config.add_section(group)
        self._config[group][key] = str(value)

    def setDefault(self, group, key, value):
        if not (group, key) in self:
            self.set(group, key, value)

    def dump(self):
        with open(self.iniPath + ".dump", "wt+") as configfile:
            self._config.write(configfile)

    @staticmethod
    @atexit.register
    def _dump():
        if CraftCore.settings.getboolean("CraftDebug", "DumpSettings", False):
            CraftCore.settings.dump()

    def cacheRepositoryUrls(self) -> list[str]:
        out = [
            "/".join(
                [
                    url if not url.endswith("/") else url[0:-1],
                    CraftCore.settings.get("Packager", "CacheVersion"),
                    *CraftCore.compiler.signature,
                ]
            )
            for url in CraftCore.settings.getList("Packager", "RepositoryUrl")
        ]
        return out
