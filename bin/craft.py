#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# this will craft some programs...

# copyright:
# Holger Schroeder <holger [AT] holgis [DOT] net>
# Patrick Spendrin <ps_ml [AT] gmx [DOT] de>
# Hannah von Reth <vonreth [AT] kde [DOT] org>

# The minimum python version for craft please edit here
# if you add code that changes this requirement

import sys

import CraftDependencies
from CraftDebug import craftDebug
import CraftTimer

import time
import datetime
import traceback
import argparse
import collections
import copy

from CraftCompiler import craftCompiler
import portageSearch
import InstallDB
import portage
import utils
import threading
from CraftConfig import *
import CraftSetupHelper

if not "KDEROOT" in os.environ:
    helper = CraftSetupHelper.SetupHelper()
    helper.subst()
    helper.setupEnvironment()
    helper.printBanner()



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
        elif not any(os.path.exists(x) and os.path.samefile(path, x) for x in [ CraftStandardDirs.downloadDir(), os.path.normpath(os.path.join(CraftStandardDirs.craftBin(), "..")),
                           os.path.join(CraftStandardDirs.craftRoot(), "python")]):
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

def packageIsOutdated( category, package ):
    newest = portage.PortageInstance.getNewestVersion( category, package )
    installed = InstallDB.installdb.getInstalledPackages(category, package)
    for pack in installed:
        version = pack.getVersion( )
        if newest != version:
            return True


def doExec( package, action, continueFlag = False ):
    with CraftTimer.Timer("%s for %s" % ( action, package ), 1 ):
        craftDebug.step("Action: %s for %s" % (action, package))
        ret = package.execute( action )
        if not ret:
            craftDebug.log.warning("Action: %s for %s FAILED" % (action, package))
        return ret or continueFlag


def handlePackage( category, packageName, buildAction, continueFlag, skipUpToDateVcs, directTargets ):
    with CraftTimer.Timer("HandlePackage %s/%s" % (category, packageName), 3) as timer:
        craftDebug.debug_line()
        craftDebug.step("Handling package: %s, action: %s" % (packageName, buildAction))

        success = True
        package = portage.PortageInstance.getPackageInstance( category, packageName )
        if package is None:
            raise CraftDependencies.PortageException("Package not found", category, packageName)

        if buildAction in [ "all", "full-package", "update", "update-all" ]:
            if craftSettings.getboolean("Packager", "UseCache", "False")\
                    and not portage.PortageInstance.isVirtualPackage(category, packageName):
                if doExec( package, "fetch-binary"):
                    return True
            success = success and doExec( package, "fetch", continueFlag )
            skip = False
            if success and skipUpToDateVcs and package.subinfo.hasSvnTarget( ):
                revision = package.sourceVersion( )
                for p in InstallDB.installdb.getInstalledPackages(category, packageName):
                    if p.getRevision( ) == revision:
                        craftDebug.step("Skipping further actions, package is up-to-date")
                        skip = True
            if not skip:
                success = success and doExec( package, "unpack", continueFlag )
                success = success and doExec( package, "compile" )
                success = success and doExec( package, "cleanimage" )
                success = success and doExec( package, "install" )
                if buildAction in [ "all", "update", "update-all" ]:
                    success = success and doExec( package, "qmerge" )
                if buildAction == "full-package" or craftSettings.getboolean("Packager", "CreateCache"):
                    if craftSettings.getboolean("Packager", "CreateCache") and craftSettings.getboolean("Packager", "CacheDirectTargetsOnly"):
                        nameRe = re.compile(".*\/.*")
                        for target in directTargets:
                            if not nameRe.match(target):
                                craftDebug.log.error("Error:\n"
                                                     "[Packager]\n"
                                                     "CacheDirectTargetsOnly = True\n"
                                                     "Only works with fully specified packages 'category/package'")
                                return False
                        if f"{category}/{packageName}" in directTargets:
                            success = success and doExec(package, "package")
                        else:
                            craftDebug.log.info("skip packaging of non direct targets")
                    else:
                        success = success and doExec( package, "package" )
                success = success or continueFlag
        elif buildAction in [ "fetch", "fetch-binary", "unpack", "configure", "compile", "make", "checkdigest",
                              "test",
                              "package", "unmerge", "cleanimage", "cleanbuild", "createpatch",
                              "geturls",
                              "print-revision",
                              "print-files"
                            ]:
            success = doExec( package, buildAction, continueFlag )
        elif buildAction == "install":
            success = doExec( package, "cleanimage" )
            success = success and doExec( package, "install", continueFlag )
        elif buildAction == "qmerge":
            #success = doExec( package, "cleanimage" )
            #success = success and doExec( package, "install")
            success = success and doExec( package, "qmerge" )
        elif buildAction == "print-source-version":
            print( "%s-%s" % ( packageName, package.sourceVersion( ) ) )
            success = True
        elif buildAction == "print-package-version":
            print( "%s-%s-%s" % (packageName, craftCompiler.getCompilerName(), package.sourceVersion()))
            success = True
        else:
            success = craftDebug.log.error("could not understand this buildAction: %s" % buildAction)

        timer.stop()
        utils.notify( "Craft %s %s" % (buildAction, "succeeded" if success else "failed"),
                      "%s of %s/%s %s after %s" % ( buildAction, category, packageName, "succeeded" if success else "failed", timer), buildAction)
        return success


def handleSinglePackage( packageName, action, args, directTargets = None ):
    packageList = [ ]
    originalPackageList = [ ]
    categoryList = [ ]

    if action == "update-all":
        installedPackages = portage.PortageInstance.getInstallables( )
        if portage.PortageInstance.isCategory( packageName ):
            craftDebug.log.debug("Updating installed packages from category " + packageName)
        else:
            craftDebug.log.debug("Updating all installed packages")
        packageList = [ ]
        for mainCategory, mainPackage in installedPackages:
            if portage.PortageInstance.isCategory( packageName ) and ( mainCategory != packageName ):
                continue
            if InstallDB.installdb.isInstalled(mainCategory, mainPackage, args.buildType) \
                    and portage.isPackageUpdateable( mainCategory, mainPackage ):
                categoryList.append( mainCategory )
                packageList.append( mainPackage )
        craftDebug.log.debug("Will update packages: " + str(packageList))
    elif packageName:
        packageList, categoryList = portage.getPackagesCategories( packageName )

    for entry in packageList:
        craftDebug.log.debug("Checking dependencies for: %s" % entry)

    deplist = []
    for mainCategory, entry in zip( categoryList, packageList ):
        if args.target:
            craftSettings.set("PortageVersions", f"{mainCategory}/{entry}", args.target)
        deplist.append(f"{mainCategory}/{entry}")

    deplist = CraftDependencies.DependencyPackage.resolveDependenciesForList(deplist, CraftDependencies.DependencyType(args.dependencyType), maxDepth=args.dependencydepth)
    # no package found
    if len( deplist ) == 0:
        category = ""
        if not packageName.find( "/" ) == -1:
            (category, package) = packageName.split( "/" )
        portageSearch.printSearch( category, packageName )
        return False

    for item in deplist:
        item.enabled = args.ignoreAllInstalled

        if args.ignoreInstalled and item.category in categoryList and item.package in packageList or packageIsOutdated(
                item.category, item.package ):
            item.enabled = True

        craftDebug.log.debug("dependency: %s" % item)
    if not deplist:
        craftDebug.log.debug("<none>")

    #for item in deplist:
    #    cat = item[ 0 ]
    #    pac = item[ 1 ]
    #    ver = item[ 2 ]

    #    if portage.isInstalled( cat, pac, ver, buildType) and updateAll and not portage.isPackageUpdateable( cat, pac, ver ):
    #        print "remove:", cat, pac, ver
    #        deplist.remove( item )

    if action == "install-deps":
        # the first dependency is the package itself - ignore it
        del deplist[ 0 ]
    elif action == "update-direct-deps":
        for item in deplist:
            item.enabled = True


    # package[0] -> category
    # package[1] -> package
    # package[2] -> version

    info = deplist[ -1 ]
    if not portage.PortageInstance.isVirtualPackage( info.category, info.package ) and \
            not action in [ "all", "install-deps"]:#not all commands should be executed on the deps if we are a virtual packages
        # if a buildAction is given, then do not try to build dependencies
        # and do the action although the package might already be installed.
        # This is still a bit problematic since packageName might not be a valid
        # package
        # for list files, we also want to handle fetching & packaging per package
        if not handlePackage( info.category, info.package, action, args.doContinue, args.update_fast, directTargets=directTargets ):
            return False

    else:
        for info in deplist:
            isVCSTarget = False

            isLastPackage = info == deplist[ -1 ]
            if args.outDateVCS or (args.outDatePackage and isLastPackage):
                isVCSTarget = portage.PortageInstance.getUpdatableVCSTargets( info.category, info.package ) != [ ]
            isInstalled = InstallDB.installdb.isInstalled(info.category, info.package)
            if ( isInstalled and not info.enabled ) and not (
                            isInstalled and (args.outDateVCS or (
                                    args.outDatePackage and isLastPackage) ) and isVCSTarget ):
                if info.package == packageName:
                    craftDebug.log.debug("already installed %s/%s" % (info.category, info.package))
                elif not info.package == packageName:
                    craftDebug.log.debug("already installed %s/%s" % (info.category, info.package))
            else:
                # in case we only want to see which packages are still to be build, simply return the package name
                if args.probe:
                    craftDebug.log.warning("pretending %s" % info)
                else:
                    if action in [ "install-deps", "update-direct-deps" ]:
                        action = "all"

                    if not handlePackage( info.category, info.package, action, args.doContinue, args.update_fast, directTargets=directTargets ):
                        craftDebug.log.error("fatal error: package %s/%s %s failed" % \
                                             ( info.category, info.package, action ))
                        return False

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

    def _addAction(self, actionName, help = None, **kwargs):
        arg = self.parser.add_argument("--%s" % actionName,
                                       help = "[Action] %s" % (help if help else ""), **kwargs)
        self.actions[arg.dest] = actionName

    def addAction(self, actionName, **kwargs):
        self._addAction(actionName, action = ActionHandler.StoreTrueAction, **kwargs)

    def addActionWithArg(self, actionName, **kwargs):
        self._addAction(actionName, action = ActionHandler.StoreAction, **kwargs)

    def parseFinalAction(self, args, defaultAction):
        '''Returns the list of actions or [defaultAction]'''
        return [self.actions[x] for x in args.ordered_args.keys()] if hasattr(args, "ordered_args") else [defaultAction]


def main( ):
    parser = argparse.ArgumentParser( prog = "craft",
                                      description = "Craft is an open source meta build system and package manager."
                                                    "It manages dependencies and builds libraries and applications from source, on Windows, Mac, Linux and FreeBSD.",
                                      epilog = """More information see the README or http://windows.kde.org/.
    Send feedback to <kde-windows@kde.org>.""" )

    parser.add_argument( "-p", "--probe", action = "store_true",
                         help = "probing: craft will only look which files it has to build according to the list of installed files and according to the dependencies of the package." )
    parser.add_argument( "--list-file", action = "store",
                         help = "Build all packages from the csv file provided" )
    _def = craftSettings.get( "General", "Options", "" )
    if _def == "": _def = []
    else: _def = _def.split( ";" )
    parser.add_argument( "--options", action = "append",
                         default = _def,
                         help = "Set craft property from string <OPTIONS>. An example for is \"cmake.openIDE=1\" see options.py for more informations." )
    parser.add_argument("--outDateVCS", action = "store_true",
                         help = "if packages from version control system sources are installed, it marks them as out of date and rebuilds them (tags are not marked as out of date)." )
    parser.add_argument( "-sz", "--outDatePackage", action = "store_true",
                         help = "similar to -z, only that it acts only on the last package, and works as normal on the rest." )
    parser.add_argument( "-q", "--stayquiet", action = "store_true",
                         dest = "stayQuiet",
                         help = "quiet: there should be no output - The verbose level should be 0" )
    parser.add_argument( "-t", "--buildtests", action = "store_true", dest = "buildTests",
                         default = craftSettings.getboolean( "Compile", "BuildTests", True ) )
    parser.add_argument( "-c", "--continue", action = "store_true", dest = "doContinue" )
    parser.add_argument("--create-cache", action="store_true", dest="createCache",
                        default=craftSettings.getboolean("Packager", "CreateCache", "False"),
                        help="Create a binary cache, the setting is overwritten by --no-cache")
    parser.add_argument("--use-cache", action="store_true", dest="useCache",
                        default=craftSettings.getboolean("Packager", "UseCache", "False"),
                        help = "Use a binary cache, the setting is overwritten by --no-cache")
    parser.add_argument("--no-cache", action="store_true", dest="noCache",
                        default=False, help = "Don't create or use the binary cache")
    parser.add_argument( "--destroy-craft-root", action = "store_true", dest = "doDestroyCraftRoot",
                         default=False, help = "DANGEROUS: Recursively delete everything in the Craft root directory besides the kdesettings.ini, the download directory and the craft folder itself" )
    parser.add_argument( "--offline", action = "store_true",
                         default = craftSettings.getboolean( "General", "WorkOffline", False ),
                         help = "do not try to connect to the internet: KDE packages will try to use an existing source tree and other packages would try to use existing packages in the download directory.\
                          If that doesn't work, the build will fail." )
    parser.add_argument( "-f", "--force", action = "store_true", dest = "forced",
                         default = craftSettings.getboolean( "General", "EMERGE_FORCED", False ) )
    parser.add_argument( "--buildtype", choices = [ "Release", "RelWithDebInfo", "MinSizeRel", "Debug" ],
                         dest = "buildType",
                         default = craftSettings.get( "Compile", "BuildType", "RelWithDebInfo" ),
                         help = "This will override the build type set in your kdesettings.ini." )
    parser.add_argument( "-v", "--verbose", action = "count",
                         default = int( craftSettings.get( "CraftDebug", "Verbose", "0" ) ),
                         help = " verbose: increases the verbose level of craft. Default is 1. verbose level 1 contains some notes from craft, all output of cmake, make and other programs that are used.\
                          verbose level 2a dds an option VERBOSE=1 to make and craft is more verbose highest level is verbose level 3." )
    parser.add_argument( "-i", "--ignoreInstalled", action = "store_true",
                         help = "ignore install: using this option will install a package over an existing install. This can be useful if you want to check some new code and your last build isn't that old." )
    parser.add_argument( "-ia", "--ignoreAllInstalled", action = "store_true",
                         help = "ignore all install: using this option will install all package over an existing install. This can be useful if you want to check some new code and your last build isn't that old." )

    parser.add_argument( "--target", action = "store",
                         help = "This will override the build of the default target." )
    parser.add_argument( "--search", action = "store_true",
                         help = "This will search for a package or a description matching or similar to the search term." )
    parser.add_argument( "--noclean", action = "store_true",
                         default = craftSettings.getboolean( "General", "EMERGE_NOCLEAN", False ),
                         help = "this option will try to use an existing build directory. Please handle this option with care - it will possibly break if the directory isn't existing." )
    parser.add_argument( "--clean", action = "store_false", dest = "noclean",
                         help = "oposite of --noclean" )
    parser.add_argument( "--patchlevel", action = "store",
                         default = craftSettings.get( "General", "EMERGE_PKGPATCHLVL", "" ),
                         help = "This will add a patch level when used together with --package" )
    parser.add_argument( "--log-dir", action = "store",
                         default = craftSettings.get( "CraftDebug", "LogDir", os.path.expanduser("~/.craft/")),
                         help = "This will log the build output to a logfile in LOG_DIR for each package. Logging information is appended to existing logs." )
    parser.add_argument( "--dt", action = "store", choices = [ "both", "runtime", "buildtime" ], default = "both",
                         dest = "dependencyType" )
    parser.add_argument( "--update-fast", action = "store_true",
                         help = "If the package is installed from svn/git and the revision did not change all steps after fetch are skipped" )
    parser.add_argument( "-d", "--dependencydepth", action = "store", type = int, default = -1,
                         help = "By default craft resolves the whole dependency graph, this option limits the depth of the graph, so a value of 1 would mean only dependencies defined in that package" )

    parser.add_argument("--src-dir", action="store", dest="srcDir",
                        help="This will override the source dir and enable the offline mode")

    parser.add_argument("--snore-settings", action="store_true", default=False, dest="snoreSettings",
                        help="Calls the notification settings")

    parser.add_argument("--ci-mode", action="store_true", default=craftSettings.getboolean("ContinuousIntegration", "Enabled", False),
                        dest="ciMode", help="Enables the ci mode")

    actionHandler = ActionHandler(parser)
    for x in sorted( [ "fetch", "fetch-binary", "unpack", "configure", "compile", "make",
                       "install", "install-deps", "qmerge", "manifest", "package", "unmerge", "test",
                       "checkdigest",
                       "full-package", "cleanimage", "cleanbuild", "createpatch", "geturls"] ):
        actionHandler.addAction( x )
    actionHandler.addAction( "update", help = "Update a single package" )

    # read-only actions
    actionHandler.addAction( "print-source-version" )
    actionHandler.addAction( "print-package-version" )
    actionHandler.addAction( "print-installed",
                             help = "This will show a list of all packages that are installed currently." )
    actionHandler.addAction( "print-revision", help = "Print the revision of the package and exit" )
    actionHandler.addAction( "print-files", help = "Print the files installed by the package and exit" )
    actionHandler.addActionWithArg( "search-file", help = "Print packages owning the file" )

    # other actions
    parser.add_argument( "packageNames", nargs = argparse.REMAINDER )

    args = parser.parse_args( )

    if args.doDestroyCraftRoot:
        destroyCraftRoot()
        return True

    if args.snoreSettings:
        snoresettigns = utils.utilsCache.findApplication("snoresettings")
        if snoresettigns:
            return utils.system("%s -a snoresend" % snoresettigns)
        return False


    if args.stayQuiet:
        craftDebug.setVerbose(-1)
    elif args.verbose:
        craftDebug.setVerbose(args.verbose)

    craftSettings.set( "General", "WorkOffline", args.offline or args.srcDir is not None )
    craftSettings.set( "General", "EMERGE_NOCLEAN", args.noclean )
    craftSettings.set( "General", "EMERGE_FORCED", args.forced )
    craftSettings.set( "Compile", "BuildTests", args.buildTests )
    craftSettings.set( "Compile", "BuildType", args.buildType )
    craftSettings.set( "General", "Options", ";".join( args.options ) )
    craftSettings.set( "CraftDebug", "LogDir", args.log_dir )
    craftSettings.set( "General", "EMERGE_PKGPATCHLVL", args.patchlevel )
    craftSettings.set( "Packager", "CreateCache", not args.noCache and args.createCache)
    craftSettings.set( "Packager", "UseCache", not args.noCache and args.useCache)
    craftSettings.set( "ContinuousIntegration", "SourceDir", args.srcDir)
    craftSettings.set( "ContinuousIntegration", "Enabled",  args.ciMode)

    if craftSettings.getboolean("Packager", "CreateCache"):
        # we are in cache creation mode, ensure to create a 7z image and not an installer
        craftSettings.set("Packager", "PackageType", "SevenZipPackager")

    portage.PortageInstance.options = args.options
    if args.search:
        for package in args.packageNames:
            category = ""
            if not package.find( "/" ) == -1:
                (category, package) = package.split( "/" )
            portageSearch.printSearch( category, package )
        return True


    for action in actionHandler.parseFinalAction(args, "all"):
        tempArgs = copy.deepcopy(args)

        if action in [ "install-deps", "update", "update-all", "package" ] or tempArgs.update_fast:
            tempArgs.ignoreInstalled = True

        if action in [ "update", "update-all" ]:
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
            InstallDB.printInstalled( )
        elif action == "search-file":
            portage.printPackagesForFileSearch(tempArgs.search_file)
        else:
            for packageName in packageNames:
                if not handleSinglePackage( packageName, action, tempArgs, packageNames):
                    return False
    return True


if __name__ == '__main__':
    success = False
    with CraftTimer.Timer("Craft", 0):
        try:
            doUpdateTitle = True

            def updateTitle( startTime, title ):
                while ( doUpdateTitle ):
                    delta = datetime.datetime.now( ) - startTime
                    utils.OsUtils.setConsoleTitle( "craft %s %s" % (title, delta) )
                    time.sleep( 1 )

            tittleThread = threading.Thread( target = updateTitle,
                                             args = (datetime.datetime.now( ), " ".join( sys.argv[ 1: ] ),) )
            tittleThread.setDaemon( True )
            tittleThread.start( )
            success = main()
        except KeyboardInterrupt:
            pass
        except CraftDependencies.PortageException as e:
            craftDebug.log.error(e, exc_info=e.exception or e)
        except Exception as e:
            craftDebug.log.error( e, exc_info=e)
        finally:
            doUpdateTitle = False

    if not success:
        exit( 1 )

