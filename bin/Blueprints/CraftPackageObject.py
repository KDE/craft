# -*- coding: utf-8 -*-
# Copyright Hannah von Reth <vonreth@kde.org>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

import copy
import configparser
import importlib
import os
import re

import utils
from CraftCore import CraftCore
from CraftStandardDirs import CraftStandardDirs
from CraftOS.osutils import OsUtils


class CategoryPackageObject(object):
    def __init__(self, localPath : str):
        self.localPath = localPath
        self.description = ""
        self.webpage = ""
        self.displayName = ""
        self.tags = ""
        self.platforms = CraftCore.compiler.Platforms.All
        self.compiler = CraftCore.compiler.Compiler.All
        self.pathOverride = None
        self.valid = False

        ini = os.path.join(self.localPath, "info.ini")
        if os.path.exists(ini):
            self.valid = True
            info = configparser.ConfigParser()
            info.read(ini)
            general = info["General"]
            self.displayName = general.get("displayName", "")
            self.description = general.get("description", "")
            self.tags = general.get("tags", "")
            self.webpage = general.get("webpage", "")
            platform = set(CraftCore.settings._parseList(general.get("platforms", "")))

            if platform:
                self.platforms = CraftCore.compiler.Platforms.NoPlatform
                for p in platform:
                    self.platforms |= CraftCore.compiler.Platforms.fromString(p)

            compiler = set(CraftCore.settings._parseList(general.get("compiler", "")))

            if compiler:
                self.compiler = CraftCore.compiler.Compiler.NoCompiler
                for c in compiler:
                    self.compiler |=  CraftCore.compiler.Compiler.fromString(c)
            self.pathOverride = general.get("pathOverride", None)
            self.forceOverride = general.get("forceOverride", False)

    @property
    def isActive(self) -> bool:
        if not CraftCore.compiler.platform & self.platforms:
            CraftCore.log.debug(f"{self.localPath}, is not supported on {CraftCore.compiler.platform!r}, supported platforms {self.platforms!r}")
            return False
        if not CraftCore.compiler.compiler & self.compiler:
            CraftCore.log.debug(f"{self.localPath}, is not supported on {CraftCore.compiler._compiler!r}, supported compiler {self.compiler!r}")
            return False
        return True

class CraftPackageObject(object):
    __rootPackage = None
    __rootDirectories = []
    # list of all leaves, unaffected by overrides etc
    _allLeaves = {}
    _recipes = {}#all recipes, for lookup by package name
    IgnoredDirectories = {"__pycache__"}
    Ignores = re.compile("a^")

    @staticmethod
    def _isDirIgnored(d):
        return d.startswith(".") or d in CraftPackageObject.IgnoredDirectories

    def __init__(self, other=None, parent=None):
        if isinstance(other, CraftPackageObject):
            self.__dict__ = other.__dict__
            return
        if other and not parent:
            raise Exception("Calling CraftPackageObject(str) directly is not supported,"
                            " use CraftPackageObject.get(str) instead.")

        self.parent = parent
        self.name = other
        self.filePath = ""
        self.children = {}
        self.source = None
        self.categoryInfo = None
        self._version = None
        self._instance = None
        self.__path = None
        self.__blueprintRoot = None

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent
        self.__path = None

    @property
    def path(self):
        if not self.__path:
            if not self.name:
                return None
            if self.name == "/":
                self.__path = self.name
            elif self.parent.path == "/":
                self.__path = self.name
            else:
                self.__path = "/".join([self.parent.path, self.name])
        return self.__path

    @staticmethod
    def get(path):
        if isinstance(path, CraftPackageObject):
            return path
        root = CraftPackageObject.root()
        package = None
        if path in CraftPackageObject._recipes:
            packages = CraftPackageObject._recipes[path]
            if len(packages) > 1:
                CraftCore.log.info(f"Found multiple recipes for {path}")
                for p in packages:
                    CraftCore.log.info(f"{p}: {p.source}")
                CraftCore.log.info(f"Please use the full path to the recipe.")
                exit(1)
            package = packages[0]
        else:
            if path == "/":
                return root
            else:
                components = path.split("/")
                package = root
                for part in components:
                    package = package.children.get(part, None)
                    if not package:
                        return None
        return package

    @staticmethod
    def _expandChildren(path, parent, blueprintRoot):
        if path:
            path = utils.normalisePath(path)
            name = path.rsplit("/", 1)[-1]
            if name in parent.children:
                package = parent.children[name]
            else:
                package = CraftPackageObject(name, parent)
                package.filePath = path
        elif blueprintRoot:
            path = blueprintRoot
            package = parent
        else:
            raise Exception("Unreachable")
        package.__blueprintRoot = blueprintRoot

        if not package.categoryInfo:
            package.categoryInfo = CategoryPackageObject(path)
            if not package.categoryInfo.valid and package.parent:
                if package.parent.__blueprintRoot == package.__blueprintRoot:
                    # we actually need a copy
                    package.categoryInfo = copy.copy(package.parent.categoryInfo)
                    if not package.categoryInfo.valid:
                        package.categoryInfo = CategoryPackageObject(blueprintRoot)

        for f in os.listdir(path):
            fPath = os.path.abspath(os.path.join(path, f))
            if os.path.isdir(fPath):
                if not CraftPackageObject._isDirIgnored(f):
                    child = CraftPackageObject._expandChildren(fPath, package, blueprintRoot)
                    if child:
                        if f in package.children:
                            existingNode = package.children[f]
                            if not existingNode.isCategory():
                                CraftCore.log.warning(
                                    f"Blueprint clash detected: Ignoring {child.source} in favour of {existingNode.source}")
                                continue
                            else:
                                #merge with existing node
                                existingNode.children.update(child.children)
                        else:
                            package.children[f] = child
            elif f.endswith(".py"):
                if package.source:
                    raise BlueprintException(f"Multiple py files in one directory: {package.source} and {f}", package)
                if f[:-3] != package.name:
                    raise BlueprintException(f"Recipes must match the name of the directory: {fPath}", package)
                package.source = fPath
                CraftPackageObject._allLeaves[package.path] = package
        if package.children and package.source:
            raise BlueprintException(f"{package} has has children but also a recipe {package.source}!", package)

        if path != blueprintRoot:
            if not package.source and not package.children:
                if os.listdir(path) in [["__pycache__"], []]:
                    # the recipe was removed
                    utils.rmtree(path)
                else:
                    CraftCore.log.warning(f"Found an dead branch in {blueprintRoot}/{package.path}\n"
                                       f"You might wan't to run \"git clean -xdf\" in that directry.")
                return None
        return package

    @staticmethod
    def rootDirectories():
        # this function should return all currently set blueprint directories
        if not CraftPackageObject.__rootDirectories:
            rootDirs = {utils.normalisePath(CraftStandardDirs.craftRepositoryDir())}
            if ("Blueprints", "Locations") in CraftCore.settings:
                for path in CraftCore.settings.getList("Blueprints", "Locations"):
                    rootDirs.add(utils.normalisePath(path))
            if os.path.isdir(CraftStandardDirs.blueprintRoot()):
                for f in os.listdir(CraftStandardDirs.blueprintRoot()):
                    if CraftPackageObject._isDirIgnored(f):
                        continue
                    rootDirs.add(utils.normalisePath(os.path.join(CraftStandardDirs.blueprintRoot(), f)))
            CraftCore.log.debug(f"Craft BlueprintLocations: {rootDirs}")
            CraftPackageObject.__rootDirectories = list(rootDirs)
        return CraftPackageObject.__rootDirectories

    @staticmethod
    def __regiserNodes(package):
        # danger, we detach here
        for child in list(package.children.values()):
            # hash leaves for direct acces
            if not child.isCategory():
                if not (not child.categoryInfo.isActive and child.categoryInfo.pathOverride):
                    CraftCore.log.debug(f"Adding package {child.source}")
                    if child.name not in CraftPackageObject._recipes:
                        CraftPackageObject._recipes[child.name] = []
                    CraftPackageObject._recipes[child.name].append(child)
            else:
                if child.categoryInfo.pathOverride:
                    # override path
                    existingNode = CraftPackageObject.get(child.categoryInfo.pathOverride)
                    if not existingNode:
                        raise BlueprintNotFoundException(child.categoryInfo.pathOverride)
                    for nodeName, node in child.children.items():
                        # reparent the packages
                        if nodeName in existingNode.children:
                            if not node.categoryInfo.isActive and not node.categoryInfo.forceOverride:
                                # don't reparent as we would override the actual package
                                continue
                            else:
                                old = existingNode.children.pop(nodeName)
                                CraftCore.log.debug(f"Overriding {old.path}({old.filePath}) with {node.path}")
                        node.parent = existingNode
                        child.parent.children[nodeName] = node
            CraftPackageObject.__regiserNodes(child)

    @staticmethod
    def root():
        if not CraftPackageObject.__rootPackage:
            if ("Blueprints", "Ignores") in CraftCore.settings:
                CraftPackageObject.Ignores = re.compile("|".join([f"^{entry}$" for entry in CraftCore.settings.get("Blueprints", "Ignores").split(";")]))

            CraftPackageObject.__rootPackage = root = CraftPackageObject()
            root.name = "/"
            for blueprintRoot in CraftPackageObject.rootDirectories():
                if not os.path.isdir(blueprintRoot):
                    CraftCore.log.warning(f"{blueprintRoot} does not exist")
                    continue
                blueprintRoot = utils.normalisePath(os.path.abspath(blueprintRoot))
                # create a dummy package to load its children
                child = CraftPackageObject._expandChildren(None, root, blueprintRoot)
                root.children.update(child.children)
            CraftPackageObject.__regiserNodes(root)
        return CraftPackageObject.__rootPackage

    @property
    def instance(self):
        if not self._instance:
            CraftCore.log.debug(f"module to import: {self.source} {self.path}")
            modulename = os.path.splitext(os.path.basename(self.source))[0].replace('.', '_')
            loader = importlib.machinery.SourceFileLoader(modulename, self.source)
            try:
                mod = loader.load_module()
            except Exception as e:
                raise BlueprintException(f"Failed to load file {self.source}", self, e)
            if not mod is None:
                mod.CRAFT_CURRENT_MODULE = self
                pack = mod.Package()
                self._instance = pack
            else:
                raise BlueprintException("Failed to find package", self)
        return self._instance

    @property
    def isInstalled(self) -> bool:
        return len(CraftCore.installdb.getInstalledPackages(self)) == 1

    @property
    def subinfo(self):
        return self.instance.subinfo

    def isCategory(self):
        return not self.source

    def isIgnored(self):
        if self.categoryInfo and not self.categoryInfo.isActive:
            return True
        import options
        if not self.path:
            return False
        ignored = options.UserOptions.get(self).ignored
        if ignored is not None:
            return ignored
        ignored = self.path and CraftPackageObject.Ignores.match(self.path)
        if ignored:
            CraftCore.log.warning(f"You are using the deprecated Ignore setting:\n"
                                  f"[Blueprints]\n"
                                  f"Ignores={self.path}\n\n"
                                  f"Please use BlueprintSettings.ini\n"
                                  f"[{self.path}]\n"
                                  f"ignored = True")
        return ignored

    @property
    def version(self):
        if self.isCategory():
            return None
        if not self._version:
            self._version = self.instance.version
        return self._version

    def __eq__(self, other):
        if isinstance(other, CraftPackageObject):
            return self.path == other.path
        return self.path == other

    def __str__(self):
        return self.path or "None"

    def __hash__(self):
        return self.path.__hash__()

    def __repr__(self):
        return f"CraftPackageObject({self.path})"

    def allChildren(self):
        recipes = []
        for p in self.children.values():
            recipes.append(p)
            recipes.extend(p.allChildren())
        return recipes


class BlueprintException(Exception):
    def __init__(self, message, package, exception=None):
        Exception.__init__(self, message)

        self.package = package
        self.exception = exception

    def __str__(self):
        return f"{self.package.source or self.package} failed:\n{Exception.__str__(self)}"


class BlueprintNotFoundException(Exception):
    def __init__(self, packageName, message=None):
        Exception.__init__(self)
        self.packageName = packageName
        self.message = message

    def __str__(self):
        if self.message:
            return self.message
        else:
            return f"Failed to find {self.packageName}: {Exception.__str__(self)}"
