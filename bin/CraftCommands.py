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
import subprocess
import tempfile
import glob
from pathlib import Path
from collections import namedtuple, OrderedDict
import urllib

import CraftBase
from Blueprints.CraftDependencyPackage import CraftDependencyPackage, DependencyType
from Blueprints.CraftVersion import CraftVersion
from Blueprints.CraftPackageObject import CraftPackageObject
from Utils.CraftTitleUpdater import CraftTitleUpdater
from Utils import CraftTimer
from options import *

import utils


def __recurseCraft(command:[str], args:[str]):
    # command is the essential action, args might get split into multiple calls
    # close the log file and the db
    UserOptions.instance()._save()
    CraftTitleUpdater.instance.stop()
    CraftCore.debug.close()
    if hasattr(CraftCore, "installdb"):
        del CraftCore.installdb
    for args in utils.limitCommandLineLength([sys.executable, sys.argv[0]] + command, args):
        if not subprocess.call(args) == 0:
            return False
    return True

def doExec(package, action):
    with CraftTimer.Timer("%s for %s" % (action, package), 1):
        CraftCore.debug.step("Action: %s for %s" % (action, package))
        ret = package.instance.runAction(action)
        if not ret:
            if action == "fetch-binary":
                CraftCore.debug.step(f"{package} not found in cache")
                return False
            CraftCore.log.warning(f"Action: {action} for {package}:{package.version} FAILED")
        return ret


# in general it would be nice to handle this with inheritance, but actually we don't wan't a blueprint to be able to change the behaviour of "all"...
def handlePackage(package, buildAction, directTargets):
    with CraftTimer.Timer(f"HandlePackage {package}", 3) as timer:
        success = True
        actions = []
        timer.hook = lambda : utils.notify(f"Craft {buildAction} {'succeeded' if success else 'failed'}", f"{package} after {timer}", buildAction)
        CraftCore.debug.debug_line()
        CraftCore.debug.step(f"Handling package: {package}, action: {buildAction}")

        if buildAction in ["all", "update"]:
            if CraftCore.settings.getboolean("Packager", "UseCache", "False"):
                if doExec(package, "fetch-binary"):
                    return True
            if buildAction == "all":
                actions = ["fetch", "unpack", "compile", "cleanimage", "install", "post-install"]
                if CraftCore.settings.getboolean("ContinuousIntegration", "ClearBuildFolder", False):
                    actions += ["cleanbuild"]
                actions += ["qmerge", "post-qmerge"]
                if CraftCore.settings.getboolean("Packager", "CreateCache"):
                    onlyDirect = CraftCore.settings.getboolean("Packager", "CacheDirectTargetsOnly")
                    if not onlyDirect or (onlyDirect and package in directTargets):
                        actions += ["package"]
            elif buildAction == "update":
                actions = ["update"]
        else:
            actions = [buildAction]
        for action in actions:
            success = doExec(package, action)
            if not success:
                return False
        return True

def resolvePackage(packageNames : [str], version : str=None) -> [CraftPackageObject]:
    package = CraftPackageObject(None)
    def resolveChildren(child):
        if child.isCategory():
            for c in child.children.values():
                resolveChildren(c)
        else:
            if version:
                UserOptions.addPackageOption(child, "version", version)
            package.children[child.name] = child

    for packageName in packageNames:
        child = CraftPackageObject.get(packageName)
        if not child:
            raise BlueprintNotFoundException(packageName)
        resolveChildren(child)
    return package


def setOption(packageNames : [str], option : str) -> bool:
    if "=" not in option:
        CraftCore.log.error(f"Invalid option {option}")
        return False
    key, value = option.split("=", 1)
    for name in packageNames:
        package = CraftPackageObject.get(name)
        if not package:
            raise BlueprintNotFoundException(name)
        # create instance to make sure options are registered
        # version is a special case, it is build in and a non existing version causes an error during construction
        # skipping the check allows to replace an invalid version
        if option != "version" and not package.isCategory():
                package.instance
        options = UserOptions.get(package)
        if not options.setOption(key, value):
            return False
        CraftCore.log.info(f"[{package}]\n{key}={getattr(options, key)}")
    return True

def addBlueprintsRepository(url : str) -> bool:
    templateDir = os.path.join(CraftCore.standardDirs.craftBin(), "..", "internal_blueprints" )
    with tempfile.TemporaryDirectory() as tmp:
        iniPath = os.path.join(tmp, "version.ini")
        parser = configparser.ConfigParser()
        parser.read(iniPath)
        parser.add_section("General")
        parser["General"]["branches"] = "master"
        parser["General"]["defaulttarget"] = "master"
        parser["General"]["gitUrl"] = url
        with open(iniPath, "wt", encoding="UTF-8") as out:
            parser.write(out)
        CraftCore.settings.set("Blueprints", "Locations", templateDir)
        CraftCore.settings.set("InternalTemp", "add-bluprints-template.ini", iniPath)
        pkg = CraftPackageObject.get("add-bluprints-template")
        if pkg._instance:
            # reset the pkg to pick up the values
            del pkg._instance
            pkg._instance = None
        return handlePackage(pkg, "fetch", [])

def destroyCraftRoot() -> bool:
    OsUtils.killProcess()
    settingsFiles = {"kdesettings.ini", "CraftSettings.ini", "BlueprintSettings.ini"}
    dirsToKeep = [CraftCore.standardDirs.downloadDir(),
                  os.path.join(CraftCore.standardDirs.craftBin(), ".."),
                  os.path.join(CraftCore.standardDirs.craftRoot(), "python"),
                  CraftCore.standardDirs.blueprintRoot()]
    # dirs with possible interesting sub dirs
    maybeKeepDir = [
        CraftCore.standardDirs.craftRoot(),
        CraftCore.standardDirs.etcDir(),
        os.path.join(CraftCore.standardDirs.etcDir(), "blueprints")# might contain blueprintRoot
        ]
    def deleteEntry(path):
        if utils.OsUtils.isLink(path):
            CraftCore.log.debug(f"Skipping symlink {path}")
            return
        if os.path.isdir(path):
            if any(os.path.exists(x) and os.path.samefile(path, x) for x in maybeKeepDir):
                CraftCore.log.debug(f"Path {path} in maybeKeepDir")
                for entry in os.listdir(path):
                    deleteEntry(os.path.join(path, entry))
            elif any(os.path.exists(x) and os.path.samefile(path, x) for x in dirsToKeep):
                CraftCore.log.debug(f"Path {path} in dirsToKeep")
            else:
                utils.cleanDirectory(path)
                utils.OsUtils.rmDir(path, True)
        else:
            if os.path.basename(path) not in settingsFiles:
                utils.OsUtils.rm(path, True)

    del CraftCore.installdb
    deleteEntry(CraftCore.standardDirs.craftRoot())
    return True


def unShelve(shelve, args):
    packageNames = []
    parser = configparser.ConfigParser(allow_no_value=True)
    parser.read(shelve, encoding="UTF-8")
    listVersion = 1
    blueprintRepositories = []
    if "General" in parser:
        listVersion = int(parser["General"].get("version", listVersion))
        blueprintRepositories = CraftCore.settings._parseList(parser["General"].get("blueprintRepositories", ""))
    for repo in blueprintRepositories:
        addBlueprintsRepository(repo)
    Info = namedtuple("Info", "version revision")
    packages = {} # type: Info
    if listVersion == 1:
        for sections in parser.keys():
            for packageName in parser[sections]:
                packages[packageName] = Info(parser[sections].get(packageName, None), None)
    elif listVersion == 2:
        for p, s in parser.items():
            if p in {"General", "DEFAULT"}:
                continue
            packages[p] = Info(s.get("version", None), s.get("revision", None))

    settings = UserOptions.instance().settings
    for p, info in packages.items():
        if (info.version or info.revision) and not settings.has_section(p):
            settings.add_section(p)
        if info.version:
            settings[p]["version"] = info.version
        if info.revision:
            settings[p]["revision"] = info.revision
    # bootstrap craft first
    return __recurseCraft([], ["craft"]) and __recurseCraft([], list(packages.keys()))

def shelve(target : str):
    target = Path(target)
    CraftCore.log.info(f"Creating shelve: {target}")
    listFile = configparser.ConfigParser(allow_no_value=True)
    updating = target.exists()
    if updating:
        listFile.read(target, encoding="UTF-8")
        oldSections = set(listFile.sections())
        if "General" in oldSections:
            oldSections.remove("General")
    if not listFile.has_section("General"):
        listFile.add_section("General")
    listFile["General"]["version"] = "2"
    blueprintRepos = []
    for p in CraftPackageObject.get("craft").children.values():
        if p.path in {"craft/craft-core", "craft/craftmaster"}:
            continue
        blueprintRepos.append(p.instance.repositoryUrl())
    listFile["General"]["blueprintRepositories"] = ";".join(blueprintRepos)
    reDate = re.compile(r"\d\d\d\d\.\d\d\.\d\d")

    def _set(package, key:str, value:str):
        if updating:
            old = package.get(key, value)
            if old != value:
                CraftCore.log.info(f"Updating {package.name} {key}: {old} -> {value}")
        package[key] = value

    newPackages = set()
    for package, version, revision in CraftCore.installdb.getDistinctInstalled():
        packageObject = CraftPackageObject.get(package)
        if not packageObject:
            CraftCore.log.warning(f"{package} is no longer known to Craft, it will not be added to the list")
            continue
        if not packageObject.subinfo.shelveAble:
            continue
        if not listFile.has_section(package):
            listFile.add_section(package)
        if updating:
            newPackages.add(package)
        package = listFile[package]
        # TODO: clean our database
        patchLvl = version.split("-", 1)
        if len(patchLvl) == 2:
            # have we encoded a date or a patch lvl?
            clean = packageObject.subinfo.options.dailyUpdate and bool(reDate.match(patchLvl[1]))
            clean |= patchLvl[0] in packageObject.subinfo.patchLevel and str(packageObject.subinfo.patchLevel[patchLvl[0]] + packageObject.categoryInfo.patchLevel) == patchLvl[1]
            if clean:
                version = patchLvl[0]
        _set(package, "version",  version)
        if version != packageObject.subinfo.defaultTarget:
            CraftCore.debug.printOut(f"For {packageObject} {version} is an update availible: {packageObject.subinfo.defaultTarget}")
        if revision:
            # sadly we combine the revision with the branch "master-1234ac"
            revParts = revision.split("-", 1)
            if len(revParts) == 2:
                _set(package, "revision",  revParts[1])
    if updating:
        removed = oldSections - newPackages
        added = newPackages - oldSections
        CraftCore.log.info(f"The following packages where removed from {target}: {removed}")
        CraftCore.log.info(f"The following packages where added to {target}: {added}")
    utils.createDir(target.parent)
    listFile._sections = OrderedDict(sorted(listFile._sections.items(), key=lambda k: k[0]))
    with open(target, "wt", encoding="UTF-8") as out:
        listFile.write(out)
    return True


def packageIsOutdated(package):
    installed = CraftCore.installdb.getInstalledPackages(package)
    if not installed:
        return True
    for pack in installed:
        version = pack.getVersion()
        if not version: continue
        cacheVersion = pack.getCacheVersion()
        if cacheVersion and cacheVersion != CraftBase.CraftBase.cacheVersion():
            # can only happen for packages installed from cache
            return True
        return package.version != version

def invoke(command : str, directTargets : [CraftPackageObject]) -> bool:
    args = {}
    key = command
    argsPattern = re.compile(r"(.+)\((.*)\)")
    argsMatch = argsPattern.findall(command)
    if argsMatch:
        key = argsMatch[0][0]
        args = eval(f"dict({','.join(argsMatch[0][1:])})")
    subs = key.split(".")
    for p in directTargets:
        instance = p.instance
        path = []
        for sub in subs:
            path += [sub]
            if hasattr(instance, sub):
                attr = getattr(instance, sub)
                if callable(attr):
                    instance = attr(**args)
                else:
                    instance = attr
            else:
                CraftCore.debug.printOut(f"{p} has no member {'.'.join(path)}", file=sys.stderr)
                return False
        CraftCore.log.debug(f"--get {command} on {p} -> {type(instance)}:{instance}")
        CraftCore.debug.printOut(instance)
    return True

def run(package : [CraftPackageObject], action : str, args) -> bool:
    if package.isIgnored():
        CraftCore.log.info(f"Skipping package because it has been ignored: {package}")
        return True
    directTargets = package.children.values()
    CraftCore.state.directTargets = directTargets

    if action == "get":
        return invoke(args.get, directTargets)
    elif action == "install-to-desktop":
        return installToDektop(directTargets)
    elif action == "create-download-cache":
        return createArchiveCache(package)
    elif action == "print-files":
        return printFiles(directTargets)
    elif args.resolve_deps or action in ["all", "install-deps", "update"]:
        # work on the dependencies
        depPackage = CraftDependencyPackage(package)
        if args.resolve_deps:
            if not args.resolve_deps.capitalize() in DependencyType.__members__:
                CraftCore.log.error(f"Invalid dependency type {args.resolve_deps}, valid types are {DependencyType.__members__}")
                return False
            depType = DependencyType.__getattr__(args.resolve_deps.capitalize())
        elif action == "install-deps":
            depType = DependencyType.Both
        else:
            depType = DependencyType.All
        depList = depPackage.getDependencies(depType=depType)

        for p in directTargets:
            # print if a direct target is disabled
            # do it after the dependencies are initialised
            if p.isIgnored():
                if not p.categoryInfo.isActive:
                    CraftCore.log.warning(f"Ignoring: {p} as it is not supported on your platform/compiler")

        packages = []
        if not args.resolve_deps:
            for item in depList:
                if not item.name:
                    continue # are we a real package
                if ((item in directTargets and (args.ignoreInstalled or (action == "update" and item.subinfo.hasSvnTarget())))
                     or packageIsOutdated(item)):
                    packages.append(item)
                    CraftCore.log.debug(f"dependency: {item}")
                elif item in directTargets:
                    CraftCore.debug.step(f"{item} is up to date, nothing to do")
        else:
            packages = depList
        if not packages:
            CraftCore.log.debug("<none>")

        if action == "install-deps":
            # we don't intend to build the package itself
            for x in directTargets:
                packages.remove(x)

        CraftTitleUpdater.usePackageProgressTitle(packages)
        while packages:
            info = packages[0]
            # in case we only want to see which packages are still to be build, simply return the package name
            if args.probe:
                CraftCore.log.warning(f"pretending {info}: {info.version}")
            else:
                if CraftCore.settings.getboolean("ContinuousIntegration", "Enabled", False):
                    CraftCore.debug.debug_line()
                    CraftCore.log.info(f"Status: {CraftTitleUpdater.instance}")
                else:
                    CraftTitleUpdater.instance.updateTitle()
                if action in ["install-deps"]:
                    action = "all"
                elif action == "update" and not info.isLatestVersionInstalled:
                    action = "all"

                if not handlePackage(info, action, directTargets=directTargets):
                    CraftCore.log.error(f"fatal error: package {info} {action} failed")
                    return False
            packages.pop(0)
    else:
        for info in directTargets:
            if not handlePackage(info, action, directTargets=directTargets):
                return False

    CraftCore.debug.new_line()
    return True

def cleanBuildFiles(cleanArchives, cleanImages, cleanInstalledImages, cleanBuildDir, packages):
    def cleanDir(dir):
        if os.path.isdir(dir):
            CraftCore.log.info(f"Cleaning: {Path(dir).resolve()}")
            utils.cleanDirectory(dir)
            utils.rmtree(dir)

    for p in packages:
        package = CraftPackageObject.get(p.path)
        if not package or package.isCategory():
            continue
        CraftCore.log.debug(f"Checking package for unused files: {p.path}")
        instance = package.instance
        version = instance.version

        if version:
            imageGlob = str(instance.imageDir()).replace(version, "*")
        else:
            imageGlob = str(instance.imageDir())

        # image directories
        if cleanImages:
            for dir in glob.glob(imageGlob):
                if package.isInstalled and not cleanInstalledImages:
                    if Path(dir) == instance.imageDir():
                        continue
                cleanDir(dir)

        # archive directory
        if cleanArchives and os.path.exists(instance.archiveDir()):
            cleanDir(instance.archiveDir())

        # build directory
        if cleanBuildDir:
            cleanDir(instance.buildDir())

def upgrade(args, argv=None) -> bool:
    ENV_KEY = "CRAFT_CORE_UPDATED"
    if ENV_KEY not in os.environ:
        if argv is None:
            argv = sys.argv[1:]
        os.environ[ENV_KEY] = "1"
        # update the core
        if not run(CraftPackageObject.get("craft"), "all", args):
            return False
        return __recurseCraft([], argv)
    else:
        package = CraftPackageObject(None)
        for packageName, _, _ in CraftCore.installdb.getDistinctInstalled():
            p = CraftPackageObject.get(packageName)
            if p:
                package.children[p.name] = p
        return run(package, "update", args)

def installToDektop(packages):
    CraftCore.settings.set("Packager", "PackageType", "DesktopEntry")
    for p in packages:
        if not p.instance.createPackage():
            return False
    return True


def printFiles(packages):
    for p in packages:
        packageList = CraftCore.installdb.getInstalledPackages(p)
        for package in packageList:
            fileList = package.getFiles()
            fileList.sort()
            for file in fileList:
                CraftCore.log.info(file[0])
    return True


def createArchiveCache(packages : CraftPackageObject):
    from Source.ArchiveSource import ArchiveSource
    from Package.VirtualPackageBase import SourceComponentPackageBase
    packages = CraftDependencyPackage(packages).getDependencies()
    for p in packages:
        if not isinstance(p.instance, ArchiveSource):
            continue
        url = p.subinfo.target()
        if isinstance(url, list):
            url = url[0]
        urlInfo = urllib.parse.urlparse(url)
        if urlInfo.hostname in {"files.kde.org", "download.kde.org", "download.qt.io"}:
            CraftCore.log.info(f"Skip mirroring of {url}, host is reliable")
            continue
        if p.instance._getFileInfoFromArchiveCache():
            # already cached
            continue
        if isinstance(p.instance, SourceComponentPackageBase):
            if not p.instance.fetch(noop=False):
                return False
        else:
            if not p.instance.fetch():
                return False
        if not (p.instance.checkDigest() and
                p.instance.generateSrcManifest()):
            return False
    return True
