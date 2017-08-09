#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# this will craft some programs...

# copyright:
# Holger Schroeder <holger [AT] holgis [DOT] net>
# Patrick Spendrin <ps_ml [AT] gmx [DOT] de>
# Hannah von Reth <vonreth [AT] kde [DOT] org>

# The minimum python version for craft please edit here
# if you add code that changes this requirement

import argparse
import collections
import threading
import time

import CraftSetupHelper
import CraftTimer
import InstallDB
import portageSearch
import utils
from CraftConfig import *
from CraftVersion import CraftVersion
from Portage.CraftDependencyPackage import DependencyType, CraftDependencyPackage
from Portage.CraftPackageObject import *

if not "KDEROOT" in os.environ:
    helper = CraftSetupHelper.SetupHelper()
    helper.subst()
    helper.setupEnvironment()
    helper.printBanner()


class TitleUpdater(object):
    def __init__(self):
        self.doUpdateTitle = True
        self.title = None
        self.timer = None
        self.dynamicMessage = None

    def run(self):
        while (self.doUpdateTitle):
            dynamicPart = ""
            if self.dynamicMessage:
                dynamicPart = f" {self.dynamicMessage()}"
            utils.OsUtils.setConsoleTitle(f"{self.title}: {self.timer}{dynamicPart}")
            time.sleep(1)

    def start(self, message, timer):
        self.title = message
        self.timer = timer
        self.doUpdateTitle = True
        tittleThread = threading.Thread(target=self.run)
        tittleThread.setDaemon(True)
        tittleThread.start()

    def stop(self):
        self.doUpdateTitle = False


    @staticmethod
    def usePackageProgressTitle(packages):
        initialSize = len(packages)
        def title():
            if not packages:
                TitleUpdater.instance.dynamicMessage = None
                return ""
            progress = int((1 - len(packages) / initialSize) * 100)
            return f"{progress}% {[x.path for x in packages]}"
        TitleUpdater.instance.dynamicMessage = title



def destroyCraftRoot():
    del InstallDB.installdb
    root = CraftStandardDirs.craftRoot()
    for entry in os.listdir(root):
        path = os.path.join(root, entry)
        if os.path.exists(CraftStandardDirs.etcDir()) and os.path.samefile(path, CraftStandardDirs.etcDir()):
            for entry in os.listdir(path):
                if not entry == "kdesettings.ini":
                    etcPath = os.path.join(path, entry)
                    if os.path.isdir(etcPath):
                        if utils.OsUtils.isLink(etcPath):
                            print("Skipping symlink %s" % etcPath)
                            continue
                        utils.cleanDirectory(etcPath)
                        utils.OsUtils.rmDir(etcPath, True)
                    else:
                        utils.OsUtils.rm(etcPath, True)
        elif not any(os.path.exists(x) and os.path.samefile(path, x) for x in [CraftStandardDirs.downloadDir(),
                                                                               os.path.normpath(os.path.join(
                                                                                       CraftStandardDirs.craftBin(),
                                                                                       "..")),
                                                                               os.path.join(
                                                                                   CraftStandardDirs.craftRoot(),
                                                                                   "python")]):
            if utils.OsUtils.isLink(path):
                print("Skipping symlink %s" % path)
                continue
            utils.cleanDirectory(path)
            utils.OsUtils.rmDir(path, True)


def readListFile(listFile):
    packageNames = []
    parser = configparser.ConfigParser(allow_no_value=True)
    parser.read(listFile)
    for sections in parser.keys():
        for packageName in parser[sections]:
            craftSettings.set("PortageVersions", packageName, parser.get(sections, packageName))
            packageNames.append(packageName)
    return packageNames


def packageIsOutdated(package):
    installed = InstallDB.installdb.getInstalledPackages(package)
    if not installed:
        return True
    for pack in installed:
        version = pack.getVersion()
        if not version: continue
        return CraftVersion(package.version) > CraftVersion(version)

def doExec(package, action, continueFlag=False):
    with CraftTimer.Timer("%s for %s" % (action, package), 1):
        craftDebug.step("Action: %s for %s" % (action, package))
        ret = package.instance.execute(action)
        if not ret:
            craftDebug.log.warning("Action: %s for %s FAILED" % (action, package))
        return ret or continueFlag


def handlePackage(package, buildAction, continueFlag, directTargets):
    with CraftTimer.Timer(f"HandlePackage {package}", 3) as timer:
        craftDebug.debug_line()
        craftDebug.step(f"Handling package: {package}, action: {buildAction}")

        success = True

        if buildAction in ["all", "full-package", "update"]:
            if craftSettings.getboolean("Packager", "UseCache", "False") \
                    and not package.isVirtualPackage():
                if doExec(package, "fetch-binary"):
                    return True
            success = success and doExec(package, "fetch", continueFlag)

            success = success and doExec(package, "unpack", continueFlag)
            success = success and doExec(package, "compile")
            success = success and doExec(package, "cleanimage")
            success = success and doExec(package, "install")
            if buildAction in ["all", "update"]:
                success = success and doExec(package, "qmerge")
            if buildAction == "full-package" or craftSettings.getboolean("Packager", "CreateCache"):
                if craftSettings.getboolean("Packager", "CreateCache") and craftSettings.getboolean("Packager",
                                                                                                    "CacheDirectTargetsOnly"):
                    nameRe = re.compile(".*\/.*")
                    for target in directTargets:
                        if not nameRe.match(target):
                            craftDebug.log.error("Error:\n"
                                                 "[Packager]\n"
                                                 "CacheDirectTargetsOnly = True\n"
                                                 "Only works with fully specified packages 'category/package'")
                            return False
                    if package in directTargets:
                        success = success and doExec(package, "package")
                    else:
                        craftDebug.log.info("skip packaging of non direct targets")
                else:
                    success = success and doExec(package, "package")
            success = success or continueFlag
        elif buildAction in ["fetch", "fetch-binary", "unpack", "configure", "compile", "make", "checkdigest",
                             "test",
                             "package", "unmerge", "cleanimage", "cleanbuild", "createpatch",
                             "geturls",
                             "print-revision",
                             "print-files"
                             ]:
            success = doExec(package, buildAction, continueFlag)
        elif buildAction == "install":
            success = doExec(package, "cleanimage")
            success = success and doExec(package, "install", continueFlag)
        elif buildAction == "qmerge":
            success = success and doExec(package, "qmerge")
        elif buildAction == "print-source-version":
            print(f"{package}-{package.instance.sourceVersion()}")
            success = True
        else:
            success = craftDebug.log.error("could not understand this buildAction: %s" % buildAction)

        timer.stop()
        utils.notify(f"Craft {buildAction} {'succeeded' if success else 'failed'}",
                     f"{package} after {timer}", buildAction)
        return success


def run(package, action, args, directTargets):
    if package.isIgnored():
        craftDebug.log.info(f"Skipping package because it has been ignored: {package}")
        return True

    if action == "get":
        key = args.get.replace("()", "")
        isMethode = args.get.endswith("()")
        for p in directTargets:
            instance = p.instance
            if hasattr(instance, key.replace("()", "")):
                attr = getattr(instance, key)
                if isMethode:
                    value = attr()
                else:
                    value = attr
                craftDebug.log.debug(value)
                print(value)
                return True
            else:
               craftDebug.log.debug(f"{p} has no member {key}")
               print(f"{p} has no member {key}", file=sys.stderr)
               return False
    elif action not in ["all", "install-deps"]:
        for info in package.children.values():
           # not all commands should be executed on the deps if we are a virtual packages
            # if a buildAction is given, then do not try to build dependencies
            # and do the action although the package might already be installed.
            # This is still a bit problematic since packageName might not be a valid
            # package
            # for list files, we also want to handle fetching & packaging per package
            if not handlePackage(info, action, args.doContinue,
                                 directTargets=directTargets):
                return False

    else:
        depPackage = CraftDependencyPackage(package)
        depList = depPackage.getDependencies(DependencyType(args.dependencyType),
                                             maxDepth=args.dependencydepth)

        packages = []
        for item in depList:
            if (args.ignoreInstalled and item in directTargets) or args.ignoreAllInstalled or packageIsOutdated(item):
                packages.append(item)
                craftDebug.log.debug(f"dependency: {item}")
        if not packages:
            craftDebug.log.debug("<none>")

        if action == "install-deps":
            # we don't intend to build the package itself
            for x in directTargets:
                packages.remove(x)

        TitleUpdater.usePackageProgressTitle(packages)
        while packages:
            info = packages[0]
            # in case we only want to see which packages are still to be build, simply return the package name
            if args.probe:
                craftDebug.log.warning(f"pretending {info}: {info.version}")
            else:
                if action in ["install-deps"]:
                    action = "all"

                if not handlePackage(info, action, args.doContinue,
                                     directTargets=directTargets):
                    craftDebug.log.error(f"fatal error: package {info} {action} failed")
                    return False
            packages.pop(0)

    craftDebug.new_line()
    return True


class ActionHandler:
    class StoreTrueAction(argparse._StoreTrueAction):
        def __call__(self, parser, namespace, values, option_string=None):
            ActionHandler.StoreAction._addOrdered(namespace, self.dest, self.const)
            super().__call__(parser, namespace, values, option_string)

    class StoreAction(argparse._StoreAction):
        """http://stackoverflow.com/a/9028031"""

        def __call__(self, parser, namespace, values, option_string=None):
            ActionHandler.StoreAction._addOrdered(namespace, self.dest, values)
            super().__call__(parser, namespace, values, option_string)

        @staticmethod
        def _addOrdered(namespace, key, value):
            if not 'ordered_args' in namespace:
                setattr(namespace, 'ordered_args', collections.OrderedDict())
            namespace.ordered_args[key] = value

    def __init__(self, parser):
        self.parser = parser
        self.actions = {}

    def _addAction(self, actionName, help=None, **kwargs):
        arg = self.parser.add_argument("--%s" % actionName,
                                       help="[Action] %s" % (help if help else ""), **kwargs)
        self.actions[arg.dest] = actionName

    def addAction(self, actionName, **kwargs):
        self._addAction(actionName, action=ActionHandler.StoreTrueAction, **kwargs)

    def addActionWithArg(self, actionName, **kwargs):
        self._addAction(actionName, action=ActionHandler.StoreAction, **kwargs)

    def parseFinalAction(self, args, defaultAction):
        '''Returns the list of actions or [defaultAction]'''
        return [self.actions[x] for x in args.ordered_args.keys()] if hasattr(args, "ordered_args") else [defaultAction]


def main():
    parser = argparse.ArgumentParser(prog="Craft",
                                     description="Craft is an open source meta build system and package manager."
                                                 "It manages dependencies and builds libraries and applications from source, on Windows, Mac, Linux and FreeBSD.",
                                     epilog="For more information visit https://community.kde.org/Craft.\n"
                                            "Send feedback to <kde-windows@kde.org>.")

    parser.add_argument("-p", "--probe", action="store_true",
                        help="probing: craft will only look which files it has to build according to the list of installed files and according to the dependencies of the package.")
    parser.add_argument("--list-file", action="store",
                        help="Build all packages from the ini file provided")
    parser.add_argument("--options", action="append",
                        default=craftSettings.getList("General", "Options", ""),
                        help="Set craft property from string <OPTIONS>. An example for is \"cmake.openIDE=1\" see options.py for more informations.")
    parser.add_argument("-q", "--stayquiet", action="store_true",
                        dest="stayQuiet",
                        help="quiet: there should be no output - The verbose level should be 0")
    parser.add_argument("-t", "--buildtests", action="store_true", dest="buildTests",
                        default=craftSettings.getboolean("Compile", "BuildTests", True))
    parser.add_argument("-c", "--continue", action="store_true", dest="doContinue")
    parser.add_argument("--create-cache", action="store_true", dest="createCache",
                        default=craftSettings.getboolean("Packager", "CreateCache", "False"),
                        help="Create a binary cache, the setting is overwritten by --no-cache")
    parser.add_argument("--use-cache", action="store_true", dest="useCache",
                        default=craftSettings.getboolean("Packager", "UseCache", "False"),
                        help="Use a binary cache, the setting is overwritten by --no-cache")
    parser.add_argument("--no-cache", action="store_true", dest="noCache",
                        default=False, help="Don't create or use the binary cache")
    parser.add_argument("--destroy-craft-root", action="store_true", dest="doDestroyCraftRoot",
                        default=False,
                        help="DANGEROUS: Recursively delete everything in the Craft root directory besides the kdesettings.ini, the download directory and the craft folder itself")
    parser.add_argument("--offline", action="store_true",
                        default=craftSettings.getboolean("General", "WorkOffline", False),
                        help="do not try to connect to the internet: KDE packages will try to use an existing source tree and other packages would try to use existing packages in the download directory.\
                          If that doesn't work, the build will fail.")
    parser.add_argument("-f", "--force", action="store_true", dest="forced",
                        default=craftSettings.getboolean("General", "EMERGE_FORCED", False))
    parser.add_argument("--buildtype", choices=["Release", "RelWithDebInfo", "MinSizeRel", "Debug"],
                        dest="buildType",
                        default=craftSettings.get("Compile", "BuildType", "RelWithDebInfo"),
                        help="This will override the build type set in your kdesettings.ini.")
    parser.add_argument("-v", "--verbose", action="count",
                        default=int(craftSettings.get("CraftDebug", "Verbose", "0")),
                        help=" verbose: increases the verbose level of craft. Default is 1. verbose level 1 contains some notes from craft, all output of cmake, make and other programs that are used.\
                          verbose level 2a dds an option VERBOSE=1 to make and craft is more verbose highest level is verbose level 3.")
    parser.add_argument("-i", "--ignoreInstalled", action="store_true",
                        help="ignore install: using this option will install a package over an existing install. This can be useful if you want to check some new code and your last build isn't that old.")
    parser.add_argument("-ia", "--ignoreAllInstalled", action="store_true",
                        help="ignore all install: using this option will install all package over an existing install. This can be useful if you want to check some new code and your last build isn't that old.")

    parser.add_argument("--target", action="store",
                        help="This will override the build of the default target.")
    parser.add_argument("--search", action="store_true",
                        help="This will search for a package or a description matching or similar to the search term.")
    parser.add_argument("--noclean", action="store_true",
                        default=craftSettings.getboolean("General", "EMERGE_NOCLEAN", False),
                        help="this option will try to use an existing build directory. Please handle this option with care - it will possibly break if the directory isn't existing.")
    parser.add_argument("--clean", action="store_false", dest="noclean",
                        help="oposite of --noclean")
    parser.add_argument("--patchlevel", action="store",
                        default=craftSettings.get("General", "EMERGE_PKGPATCHLVL", ""),
                        help="This will add a patch level when used together with --package")
    parser.add_argument("--log-dir", action="store",
                        default=craftSettings.get("CraftDebug", "LogDir", os.path.expanduser("~/.craft/")),
                        help="This will log the build output to a logfile in LOG_DIR for each package. Logging information is appended to existing logs.")
    parser.add_argument("--dt", action="store", choices=["both", "runtime", "buildtime"], default="both",
                        dest="dependencyType")
    parser.add_argument("-d", "--dependencydepth", action="store", type=int, default=-1,
                        help="By default craft resolves the whole dependency graph, this option limits the depth of the graph, so a value of 1 would mean only dependencies defined in that package")

    parser.add_argument("--src-dir", action="store", dest="srcDir",
                        help="This will override the source dir and enable the offline mode")

    parser.add_argument("--ci-mode", action="store_true",
                        default=craftSettings.getboolean("ContinuousIntegration", "Enabled", False),
                        dest="ciMode", help="Enables the ci mode")

    actionHandler = ActionHandler(parser)
    for x in sorted(["fetch", "fetch-binary", "unpack", "configure", "compile", "make",
                     "install", "install-deps", "qmerge", "manifest", "package", "unmerge", "test",
                     "checkdigest",
                     "full-package", "cleanimage", "cleanbuild", "createpatch", "geturls"]):
        actionHandler.addAction(x)
    actionHandler.addAction("update", help="Update a single package")

    # read-only actions
    actionHandler.addAction("print-source-version")
    actionHandler.addAction("print-installed",
                            help="This will show a list of all packages that are installed currently.")
    actionHandler.addAction("print-revision", help="Print the revision of the package and exit")
    actionHandler.addAction("print-files", help="Print the files installed by the package and exit")
    actionHandler.addActionWithArg("search-file", help="Print packages owning the file")
    actionHandler.addActionWithArg("get", help="Get any value from a recipe")

    # other actions

    parser.add_argument("--version", action="version", version = f"%(prog)s {CraftSetupHelper.SetupHelper.CraftVersion}")
    parser.add_argument("packageNames", nargs=argparse.REMAINDER)

    args = parser.parse_args()

    if args.doDestroyCraftRoot:
        destroyCraftRoot()
        return True
    InstallDB.installdb.migrateDatabase()

    if args.stayQuiet:
        craftDebug.setVerbose(-1)
    elif args.verbose:
        craftDebug.setVerbose(args.verbose)

    craftSettings.set("General", "WorkOffline", args.offline or args.srcDir is not None)
    craftSettings.set("General", "EMERGE_NOCLEAN", args.noclean)
    craftSettings.set("General", "EMERGE_FORCED", args.forced)
    craftSettings.set("Compile", "BuildTests", args.buildTests)
    craftSettings.set("Compile", "BuildType", args.buildType)
    craftSettings.set("General", "Options", ";".join(args.options))
    craftSettings.set("CraftDebug", "LogDir", args.log_dir)
    craftSettings.set("General", "EMERGE_PKGPATCHLVL", args.patchlevel)
    craftSettings.set("Packager", "CreateCache", not args.noCache and args.createCache)
    craftSettings.set("Packager", "UseCache", not args.noCache and args.useCache)
    craftSettings.set("ContinuousIntegration", "SourceDir", args.srcDir)
    craftSettings.set("ContinuousIntegration", "Enabled", args.ciMode)

    if craftSettings.getboolean("Packager", "CreateCache"):
        # we are in cache creation mode, ensure to create a 7z image and not an installer
        craftSettings.set("Packager", "PackageType", "SevenZipPackager")

    CraftPackageObject.options = args.options
    if args.search:
        for package in args.packageNames:
            portageSearch.printSearch(package)
        return True

    for action in actionHandler.parseFinalAction(args, "all"):
        tempArgs = copy.deepcopy(args)

        if action in ["install-deps", "update", "package"]:
            tempArgs.ignoreInstalled = True

        if action in ["update"]:
            tempArgs.noclean = True

        craftDebug.log.debug("buildAction: %s" % action)
        craftDebug.log.debug("doPretend: %s" % tempArgs.probe)
        craftDebug.log.debug("packageName: %s" % tempArgs.packageNames)
        craftDebug.log.debug("buildType: %s" % tempArgs.buildType)
        craftDebug.log.debug("buildTests: %s" % tempArgs.buildTests)
        craftDebug.log.debug("verbose: %d" % craftDebug.verbose())
        craftDebug.log.debug("KDEROOT: %s" % CraftStandardDirs.craftRoot())

        packageNames = tempArgs.packageNames
        if tempArgs.list_file:
            if not packageNames:
                packageNames = []
            packageNames += readListFile(args.list_file)

        if action == "print-installed":
            InstallDB.printInstalled()
        elif action == "search-file":
            InstallDB.printPackagesForFileSearch(tempArgs.search_file)
        else:
            if not args.packageNames and not args.list_file:
                CraftSetupHelper.SetupHelper().printBanner()
                return True

            package = CraftPackageObject(None)
            for packageName in packageNames:
                child = CraftPackageObject.get(packageName)
                if not child:
                    portageSearch.printSearch(packageName)
                    return False

                if child.isCategory():
                    package.children = child.children
                else:
                    if tempArgs.target:
                        craftSettings.set("PortageVersions", child.path, args.target)
                    package.children[child.name] = child
            if not run(package, action, tempArgs, package.children.values()):
                return False
    return True


if __name__ == '__main__':
    success = False
    with CraftTimer.Timer("Craft", 0) as timer:
        TitleUpdater.instance = TitleUpdater()
        TitleUpdater.instance.start(f"({CraftStandardDirs.craftRoot()}) craft " + " ".join(sys.argv[1:]), timer)
        try:
            success = main()
        except KeyboardInterrupt:
            pass
        except PortageException as e:
            craftDebug.log.error(e, exc_info=e.exception or e)
        except Exception as e:
            craftDebug.log.error(e, exc_info=e)
        finally:
            TitleUpdater.instance.stop()
    if not success:
        exit(1)
