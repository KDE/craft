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

import configparser
import importlib.util
import os
from pathlib import Path
from typing import TYPE_CHECKING

import utils
from CraftCore import CraftCore
from CraftStandardDirs import CraftStandardDirs
from Utils.CraftBool import CraftBool

if TYPE_CHECKING:
    from BuildSystem.BuildSystemBase import BuildSystemBase


class CategoryPackageObject(object):
    def __init__(self, blueprintRoot, localPath: str):
        self.localPath = Path(localPath)
        self.description = ""
        self.webpage = ""
        self.displayName = ""
        self.tags = ""
        self.platforms = CraftCore.compiler.Platforms.All
        self.compiler = CraftCore.compiler.Compiler.All
        self.architecture = CraftCore.compiler.Architecture.All
        self.pathOverride = None
        self.valid = False
        self.patchLevel = 0

        self.runtimeDependencies = []
        self.buildDependencies = []

        # TODO: cache or fix handling of actual parent vs mounted parent
        # /dev-utils vs craft-blueprints-kde/dev-utils
        self._ini = self.localPath / "info.ini"
        while not self._ini.exists() and self._ini.parent.parent != blueprintRoot.parent:
            self._ini = self._ini.parent.parent / "info.ini"
        if self._ini.exists():
            self.valid = True
            info = configparser.ConfigParser()
            info.read(self._ini)
            general = info["General"]
            self.displayName = general.get("displayName", "")
            self.description = general.get("description", "")
            self.tags = general.get("tags", "")
            self.webpage = general.get("webpage", "")
            self.patchLevel = int(general.get("patchLevel", "0"))
            self.runtimeDependencies = CraftCore.settings._parseList(general.get("runtimeDependencies", ""))
            self.buildDependencies = CraftCore.settings._parseList(general.get("buildDependencies", ""))

            def readCompileFlags(key: str, default: CraftCore.compiler.CompilerFlags):
                values = set(CraftCore.settings._parseList(general.get(key, "")))
                if not values:
                    return default
                value = ~default.All
                for v in values:
                    old = value
                    if v.startswith("~"):
                        # invert the value
                        value |= ~default.fromString(v[1:])
                    else:
                        value |= default.fromString(v)

                    if old == value:
                        CraftCore.log.warning(f"{self.localPath}: The value {v!r} for {default.__class__.__name__} has no effect, values are:{values!r}")
                return value

            self.platforms = readCompileFlags("platforms", self.platforms)
            self.compiler = readCompileFlags("compiler", self.compiler)
            self.architecture = readCompileFlags("architecture", self.architecture)

            self.pathOverride = general.get("pathOverride", None)
            self.forceOverride = general.get("forceOverride", False)

    @property
    def isActive(self) -> CraftBool:
        if not CraftCore.compiler.platform.matchKeys(self.platforms):
            CraftCore.log.debug(f"{self.localPath}, is not supported on {CraftCore.compiler.platform!r}, supported platforms {self.platforms!r}")
            return CraftBool(False)
        if not CraftCore.compiler.compiler.matchKeys(self.compiler):
            CraftCore.log.debug(f"{self.localPath}, is not supported on {CraftCore.compiler.compiler!r}, supported compiler {self.compiler!r}")
            return CraftBool(False)
        if not CraftCore.compiler.architecture.matchKeys(self.architecture):
            CraftCore.log.debug(f"{self.localPath}, is not supported on {CraftCore.compiler.architecture!r}, supported architecture {self.architecture!r}")
            return CraftBool(False)
        return CraftBool(True)


class CraftPackageObject(object):
    __rootPackage = None
    __rootDirectories = []
    # list of all leaves, unaffected by overrides etc
    _allLeaves = {}
    _recipes = {}  # all recipes, for lookup by package name
    IgnoredDirectories = {"__pycache__", "LICENSES"}

    @staticmethod
    def _isDirIgnored(d):
        return d.startswith(".") or d in CraftPackageObject.IgnoredDirectories

    def __init__(self, other=None, parent=None):
        if isinstance(other, CraftPackageObject):
            self.__dict__ = other.__dict__
            return
        if other and not parent:
            raise Exception("Calling CraftPackageObject(str) directly is not supported," " use CraftPackageObject.get(str) instead.")

        self.parent = parent
        self.name = other
        self.filePath = ""
        self.children = {}
        self.source = None
        self._pattern = None
        self.categoryInfo = None  # type:CategoryPackageObject
        self._version = None
        self._instance = None
        self.__path = None

    @property
    def pattern(self) -> "BuildSystemBase":
        if not self.source:
            raise BlueprintException(f"{self.source} dos not provide a Pattern", self)
        if not self.isCategory():
            raise BlueprintException("Only a catergory can provide a Pattern", self)
        # load the module
        self.instance
        if self._pattern:
            return self._pattern

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
                CraftCore.log.info("Please use the full path to the recipe.")
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
    def _expandChildren(path, parent, blueprintRoot: Path):
        if path:
            path = Path(path)
            name = path.name
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

        if not package.categoryInfo:
            package.categoryInfo = CategoryPackageObject(blueprintRoot, path)

        for f in os.listdir(path):
            fPath = os.path.abspath(os.path.join(path, f))
            if os.path.isdir(fPath):
                if not CraftPackageObject._isDirIgnored(f):
                    child = CraftPackageObject._expandChildren(fPath, package, blueprintRoot)
                    if child:
                        if f in package.children:
                            existingNode = package.children[f]
                            if not existingNode.isCategory():
                                CraftCore.log.warning(f"Blueprint clash detected: Ignoring {child.source} in favour of {existingNode.source}")
                                continue
                            else:
                                # merge with existing node
                                existingNode.children.update(child.children)
                        else:
                            package.children[f] = child
            elif f.endswith(".py"):
                if package.source:
                    raise BlueprintException(
                        f"Multiple py files in one directory: {package.source} and {f}",
                        package,
                    )
                if f[:-3] != package.name:
                    raise BlueprintException(
                        f"Recipes must match the name of the directory: {fPath}",
                        package,
                    )
                package.source = fPath
                CraftPackageObject._allLeaves[package.path] = package

        if path != blueprintRoot:
            if not package.source and not package.children:
                if os.listdir(path) in [["__pycache__"], []]:
                    # the recipe was removed
                    utils.rmtree(path)
                else:
                    CraftCore.log.warning(
                        f"Found an dead branch in {blueprintRoot}/{package.path}\n" f'You might wan\'t to run "git clean -xdf" in that directry.'
                    )
                return None
        return package

    @staticmethod
    def rootDirectories():
        # this function should return all currently set blueprint directories
        if not CraftPackageObject.__rootDirectories:
            rootDirs = {CraftStandardDirs.craftRepositoryDir()}
            if ("Blueprints", "Locations") in CraftCore.settings:
                for path in CraftCore.settings.getList("Blueprints", "Locations"):
                    rootDirs.add(Path(path).resolve())
            if os.path.isdir(CraftStandardDirs.blueprintRoot()):
                for f in os.listdir(CraftStandardDirs.blueprintRoot()):
                    if CraftPackageObject._isDirIgnored(f):
                        continue
                    rootDirs.add((CraftStandardDirs.blueprintRoot() / f).resolve())
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
                    child.parent = existingNode
                    for nodeName, node in child.children.items():
                        node.parent = existingNode
                        # reparent the packages
                        if nodeName in existingNode.children:
                            if not node.categoryInfo.isActive and not node.categoryInfo.forceOverride:
                                continue
                            else:
                                old = existingNode.children.pop(nodeName)
                                CraftCore.log.debug(f"Overriding {old.path}({old.filePath}) with {node.path}")
                        child.parent.children[nodeName] = node
            CraftPackageObject.__regiserNodes(child)

    @staticmethod
    def root():
        if not CraftPackageObject.__rootPackage:
            CraftPackageObject.__rootPackage = root = CraftPackageObject()
            root.name = "/"
            for blueprintRoot in CraftPackageObject.rootDirectories():
                if not blueprintRoot.is_dir():
                    CraftCore.log.warning(f"{blueprintRoot} does not exist")
                    continue
                blueprintRoot = blueprintRoot.absolute()
                # create a dummy package to load its children
                child = CraftPackageObject._expandChildren(None, root, blueprintRoot)
                root.children.update(child.children)
            CraftPackageObject.__regiserNodes(root)
        return CraftPackageObject.__rootPackage

    @property
    def instance(self):
        if not self._instance and not self._pattern and self.source:
            CraftCore.log.debug(f"module to import: {self.source} {self.path}")
            modulename = os.path.splitext(os.path.basename(self.source))[0].replace(".", "_")
            try:
                spec = importlib.util.spec_from_file_location(modulename, self.source)
                self._Module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(self._Module)
            except Exception as e:
                raise BlueprintException(f"Failed to load file {self.source}", self, e)
            if self._Module is not None:
                if hasattr(self._Module, "Package"):
                    try:
                        pack = self._Module.Package(package=self)
                    except Exception as e:
                        raise BlueprintException(f"Failed to load package {self.source}", self, e)
                    # poor mans inheritance check
                    if self.children and "VirtualPackageBase" not in [x.__name__ for x in pack.__class__.__bases__]:
                        raise BlueprintException(
                            f"{self} is a category and may only provide a Pattern not a Package!",
                            self,
                        )
                    self._instance = pack
                else:
                    self._pattern = self._Module.Pattern
            else:
                raise BlueprintException("Failed to find package", self)
        return self._instance

    @property
    def isInstalled(self) -> CraftBool:
        # using the version here might cause a recursion...
        return CraftBool(CraftCore.installdb.isInstalled(self))

    @property
    def isLatestVersionInstalled(self) -> CraftBool:
        return CraftBool(CraftCore.installdb.isInstalled(self, self.version))

    @property
    def subinfo(self):
        return self.instance.subinfo

    def isCategory(self) -> CraftBool:
        return CraftBool(bool(self.children))

    def isIgnored(self) -> CraftBool:
        if self.categoryInfo and not self.categoryInfo.isActive:
            return CraftBool(True)
        import options

        if not self.path:
            return CraftBool(False)
        return CraftBool(options.UserOptions.get(self).ignored)

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
