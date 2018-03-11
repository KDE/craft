# -*- coding: utf-8 -*-
# central instance for managing settings regarding craft
# copyright:
# Hannah von Reth <vonreth [AT] kde [DOT] org>

import atexit
import configparser
import os
import shutil
import sys


from CraftCore import CraftCore

class CraftConfig(object):
    __RootDir = None

    def __init__(self, iniPath=None):
        self._config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        if iniPath:
            self.iniPath = iniPath
        else:
            oldPath = os.path.join(CraftConfig._craftRoot(), "etc", "kdesettings.ini")
            newPath = os.path.join(CraftConfig._craftRoot(), "etc", "CraftSettings.ini")
            if os.path.isfile(oldPath):
                shutil.move(oldPath, newPath)
            self.iniPath = os.path.join(newPath)
        self._alias = {}
        self._groupAlias = {}
        self._readSettings()

        if self.version < 4:
            self._setAliasesV3()

        if self.version < 5:
            self._setAliasesV4()

        self._warned = set()

    @staticmethod
    def _craftRoot():
        if CraftConfig.__RootDir:
            return CraftConfig.__RootDir
        dir = os.path.abspath(os.path.dirname(sys.argv[0]))
        while dir.count(os.path.sep) > 1 and not os.path.isfile(os.path.join(dir, "craftenv.ps1")):
            dir = os.path.dirname(dir)
        if not os.path.join(dir, "craftenv.ps1"):
            print("Failed to find the craft root", file=sys.stderr)
            exit(-1)
        CraftConfig.__RootDir = os.path.abspath(os.path.join(dir, ".."))
        return CraftConfig.__RootDir

    def _setAliasesV4(self):
        self.addGroupAlias("Blueprints", "Portage")
        self.addGroupAlias("BlueprintVersions", "PortageVersions")
        self.addAlias("Blueprints", "Locations", "General", "Portages")

    def _setAliasesV3(self):
        self.addAlias("General", "Options", "General", "EMERGE_OPTIONS")
        self.addAlias("General", "Notify", "General", "EMERGE_USE_NOTIFY")
        self.addAlias("General", "Portages", "General", "EMERGE_PORTAGE_ROOT")
        self.addAlias("CraftDebug", "LogDir", "General", "EMERGE_LOG_DIR")
        self.addAlias("ShortPath", "GitDrive", "ShortPath", "EMERGE_GIT_DRIVE")
        self.addAlias("ShortPath", "RootDrive", "ShortPath", "EMERGE_ROOT_DRIVE")
        self.addAlias("ShortPath", "DownloadDrive", "ShortPath", "EMERGE_DOWNLOAD_DRIVE")
        self.addAlias("ShortPath", "Enabled", "ShortPath", "EMERGE_USE_SHORT_PATH")

    def _warnDeprecated(self, deprecatedSection, deprecatedKey, section, key):
        if not (deprecatedSection, deprecatedKey) in self._warned:
            self._warned.add((deprecatedSection, deprecatedKey))
            print(
                f"Warning: {deprecatedSection}/{deprecatedKey} is deprecated and has been renamed to "
                f"{section}/{key}, please update your CraftSettings.ini",
                file=sys.stderr if not CraftCore.settings.getboolean("ContinuousIntegration", "Enabled", False) else sys.stdout)

    def _readSettings(self):
        if not os.path.exists(self.iniPath):
            print("Could not find config: %s" % self.iniPath, file=sys.stderr)
            return

        craftDir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        # read defaults
        self._config.read(os.path.join(craftDir, "etc", "CraftCoreSettings.ini"))
        #####
        if not "Variables" in self._config.sections():
            self._config.add_section("Variables")
        for key, value in {
            "CraftRoot": CraftConfig._craftRoot(),
            "CraftDir": craftDir }.items():
            self._config["Variables"][key] = value
        # read user settings
        self._config.read(self.iniPath)

    def __contains__(self, key):
        return self.__contains_no_alias(key) or \
               (key in self._alias and self.__contains__(self._alias[key])) or \
               (key[0] in self._groupAlias and self.__contains__((self._groupAlias[key[0]], key[1])))

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

        if default != None:
            return default
        print("Failed to find")
        print("\t[%s]" % group)
        print("\t%s = ..." % key)
        print("in your CraftSettings.ini")
        exit(1)

    @staticmethod
    def _parseList(s : str) -> [str]:
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
        with open(self.iniPath + ".dump", 'wt+') as configfile:
            self._config.write(configfile)

    @staticmethod
    @atexit.register
    def _dump():
        if CraftCore.settings.getboolean("CraftDebug", "DumpSettings", False):
            CraftCore.settings.dump()
