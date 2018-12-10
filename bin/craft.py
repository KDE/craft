#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright Holger Schroeder <holger [AT] holgis [DOT] net>
# Copyright Patrick Spendrin <ps_ml [AT] gmx [DOT] de>
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

import argparse
import collections
import sys

import CraftCommands
import CraftSetupHelper
import InstallDB
import blueprintSearch
from Blueprints.CraftPackageObject import *
from CraftCore import CraftCore
from Utils import CraftTimer
from Utils.CraftTitleUpdater import CraftTitleUpdater
from options import UserOptions

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
                                     description="Craft is an open source meta build system and package manager."
                                                 "It manages dependencies and builds libraries and applications from source, on Windows, Mac, Linux and FreeBSD.",
                                     epilog="For more information visit https://community.kde.org/Craft.\n"
                                            "Send feedback to <kde-windows@kde.org>.")

    parser.add_argument("-p", "--probe", action="store_true",
                        help="probing: craft will only look which files it has to build according to the list of installed files and according to the dependencies of the package.")
    parser.add_argument("--list-file", action="store",
                        help="Build all packages from the ini file provided")
    parser.add_argument("--options", action="append",
                        default=CraftCore.settings.getList("General", "Options", ""),
                        help="Set craft property from string <OPTIONS>. An example for is \"cmake.openIDE=1\" see options.py for more informations.")
    parser.add_argument("-q", "--stayquiet", action="store_true",
                        dest="stayQuiet",
                        help="quiet: there should be no output - The verbose level should be 0")
    parser.add_argument("--create-cache", action="store_true", dest="createCache",
                        default=CraftCore.settings.getboolean("Packager", "CreateCache", "False"),
                        help="Create a binary cache, the setting is overwritten by --no-cache")
    parser.add_argument("--use-cache", action="store_true", dest="useCache",
                        default=CraftCore.settings.getboolean("Packager", "UseCache", "False"),
                        help="Use a binary cache, the setting is overwritten by --no-cache")
    parser.add_argument("--no-cache", action="store_true", dest="noCache",
                        default=False, help="Don't create or use the binary cache")
    parser.add_argument("--destroy-craft-root", action="store_true", dest="doDestroyCraftRoot",
                        default=False,
                        help="DANGEROUS: Recursively delete everything in the Craft root directory besides the CraftSettings.ini, the download directory and the craft folder itself")
    parser.add_argument("--offline", action="store_true",
                        default=CraftCore.settings.getboolean("General", "WorkOffline", False),
                        help="do not try to connect to the internet: KDE packages will try to use an existing source tree and other packages would try to use existing packages in the download directory.\
                          If that doesn't work, the build will fail.")
    parser.add_argument("--buildtype", choices=["Release", "RelWithDebInfo", "MinSizeRel", "Debug"],
                        dest="buildType",
                        default=CraftCore.settings.get("Compile", "BuildType", "RelWithDebInfo"),
                        help="This will override the build type set in your CraftSettings.ini.")
    parser.add_argument("-v", "--verbose", action="count",
                        default=int(CraftCore.settings.get("CraftDebug", "Verbose", "0")),
                        help=" verbose: increases the verbose level of craft. Default is 1. verbose level 1 contains some notes from craft, all output of cmake, make and other programs that are used.\
                          verbose level 2a dds an option VERBOSE=1 to make and craft is more verbose highest level is verbose level 3.")
    parser.add_argument("-i", "--ignoreInstalled", action="store_true",
                        help="ignore install: using this option will install a package over an existing install. This can be useful if you want to check some new code and your last build isn't that old.")
    parser.add_argument("--resolve-deps", action="store", help="Similar to -i, all dependencies will be resolved and the action is applied on them")
    parser.add_argument("--target", action="store",
                        help="This will override the build of the default target.")
    parser.add_argument("--search", action="store_true",
                        help="This will search for a package or a description matching or similar to the search term.")
    parser.add_argument("--src-dir", action="store", dest="srcDir",
                        help="This will override the source dir and enable the offline mode")

    parser.add_argument("--ci-mode", action="store_true",
                        default=CraftCore.settings.getboolean("ContinuousIntegration", "Enabled", False),
                        dest="ciMode", help="Enables the ci mode")

    parser.add_argument("--add-blueprint-repository", action="store", help="Installs a blueprint repository", metavar="URL")

    actionHandler = ActionHandler(parser)
    for x in sorted(["fetch", "fetch-binary", "unpack", "configure", ("compile",{"help":"Same as --configure --make"}), "make",
                     "install", "install-deps", "qmerge", "post-qmerge", "post-install", "package", "unmerge", "test", "createpatch"], key=lambda x: x[0] if isinstance(x, tuple) else x):
        if isinstance(x, tuple):
            actionHandler.addAction(x[0], **x[1])
        else:
            actionHandler.addAction(x)

    actionHandler.addAction("update", help="Update all installed packages")
    # read-only actions
    actionHandler.addAction("print-installed",
                            help="This will show a list of all packages that are installed currently.")
    actionHandler.addAction("print-files", help="Print the files installed by the package and exit")
    actionHandler.addActionWithArg("search-file", help="Print packages owning the file")
    actionHandler.addActionWithArg("get", help="Get any value from a Blueprint")
    actionHandler.addActionWithArg("set", help="Permanently set a config value of a Blueprint")
    actionHandler.addActionWithArg("run", nargs="+", help="Run an application in the Craft environment")
    actionHandler.addAction("clean-unused", help="Clean unused files of all packages")

    # other actions

    parser.add_argument("--version", action="version", version = f"%(prog)s {CraftSetupHelper.SetupHelper.CraftVersion}")
    parser.add_argument("packageNames", nargs=argparse.REMAINDER)

    args = parser.parse_args()

    if args.stayQuiet:
        CraftCore.debug.setVerbose(-1)
    elif args.verbose:
        CraftCore.debug.setVerbose(args.verbose)

    CraftCore.settings.set("General", "WorkOffline", args.offline or args.srcDir is not None)
    CraftCore.settings.set("Compile", "BuildType", args.buildType)
    CraftCore.settings.set("General", "Options", ";".join(args.options))
    CraftCore.settings.set("Packager", "CreateCache", not args.noCache and args.createCache)
    CraftCore.settings.set("Packager", "UseCache", not args.noCache and args.useCache)
    CraftCore.settings.set("ContinuousIntegration", "SourceDir", args.srcDir)
    CraftCore.settings.set("ContinuousIntegration", "Enabled", args.ciMode)


    helper = CraftSetupHelper.SetupHelper()
    if not "KDEROOT" in os.environ:
        helper.setupEnvironment()
    helper.printBanner()


    if args.doDestroyCraftRoot:
        return CraftCommands.destroyCraftRoot()

    if args.run:
        return utils.system(args.run, shell=True)

    if args.add_blueprint_repository:
        return CraftCommands.addBlueprintsRepository(args.add_blueprint_repository, args)

    if CraftCore.settings.getboolean("Packager", "CreateCache"):
        # we are in cache creation mode, ensure to create a 7z image and not an installer
        CraftCore.settings.set("Packager", "PackageType", "SevenZipPackager")

    UserOptions.setOptions(args.options)
    if args.search:
        for package in args.packageNames:
            blueprintSearch.printSearch(package)
        return True

    for action in actionHandler.parseFinalAction(args, "all"):
        tempArgs = copy.deepcopy(args)

        if action in ["install-deps", "package"]:
            tempArgs.ignoreInstalled = True

        CraftCore.log.debug("buildAction: %s" % action)
        CraftCore.log.debug("doPretend: %s" % tempArgs.probe)
        CraftCore.log.debug("packageName: %s" % tempArgs.packageNames)
        CraftCore.log.debug("buildType: %s" % tempArgs.buildType)
        CraftCore.log.debug("verbose: %d" % CraftCore.debug.verbose())
        CraftCore.log.debug("Craft: %s" % CraftCore.standardDirs.craftRoot())

        packageNames = tempArgs.packageNames
        if tempArgs.list_file:
            if not os.path.exists(tempArgs.list_file):
                CraftCore.log.error(f"List file {tempArgs.list_file!r} does not exist")
                return False
            if not packageNames:
                packageNames = []
            packageNames += CraftCommands.readListFile(tempArgs.list_file)

        if action == "print-installed":
            InstallDB.printInstalled()
        elif action == "search-file":
            InstallDB.printPackagesForFileSearch(tempArgs.search_file)
        elif action == "set":
            CraftCommands.setOption(packageNames, args.set)
        elif action == "clean-unused":
            CraftCommands.cleanBuildFiles(cleanArchives=True, cleanImages=True, cleanInstalledImages=False, cleanBuildDir=True, packages=blueprintSearch.packages())
        elif action == "update":
            return CraftCommands.updateInstalled(tempArgs)
        else:
            if not packageNames:
                return True
            package = CraftCommands.resolvePackage(packageNames, version=tempArgs.target)
            if not CraftCommands.run(package, action, tempArgs):
                return False
    return True


if __name__ == '__main__':
    success = False
    with CraftTimer.Timer("Craft", 0) as timer:
        CraftTitleUpdater.instance = CraftTitleUpdater()
        if not "CRAFT_NOTITLEUPDATE" in os.environ and not "--ci-mode" in sys.argv:
            CraftTitleUpdater.instance.start(f"({CraftCore.standardDirs.craftRoot()}) craft " + " ".join(sys.argv[1:]), timer)
        try:
            success = main()
        except KeyboardInterrupt:
            pass
        except BlueprintNotFoundException as e:
                CraftCore.log.error(e)
                blueprintSearch.printSearch(e.packageName)
        except BlueprintException as e:
            if 0 <= CraftCore.debug.verbose() < 2:
                CraftCore.log.error(e)
                CraftCore.log.debug(e, exc_info=e.exception or e)
            else:
                CraftCore.log.error(e, exc_info=e.exception or e)
        except Exception as e:
            CraftCore.log.error(e, exc_info=e)
        finally:
            CraftTitleUpdater.instance.stop()
    if not success:
        exit(1)
