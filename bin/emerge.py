# -*- coding: utf-8 -*-
# this will emerge some programs...

# copyright:
# Holger Schroeder <holger [AT] holgis [DOT] net>
# Patrick Spendrin <ps_ml [AT] gmx [DOT] de>
# Patrick von Reth <vonreth [AT] kde [DOT] org>

# The minimum python version for emerge please edit here
# if you add code that changes this requirement

import sys

MIN_PY_VERSION = (3, 4, 0)

if sys.version_info[ 0:3 ] < MIN_PY_VERSION:
    print( "Error: Python too old!", file = sys.stderr )
    print( "Emerge needs at least Python Version %s.%s.%s" % MIN_PY_VERSION, file = sys.stderr )
    print( "Please install it and adapt your kdesettings.bat", file = sys.stderr )
    exit( 1 )

import time
import datetime
import traceback
import argparse

import compiler
import portageSearch
from InstallDB import *
from EmergeConfig import *
import jenkins


def packageIsOutdated( category, package ):
    newest = portage.PortageInstance.getNewestVersion( category, package )
    installed = installdb.getInstalledPackages( category, package )
    for pack in installed:
        version = pack.getVersion( )
        if newest != version:
            return True


@utils.log
def doExec( package, action, continueFlag = False ):
    utils.startTimer( "%s for %s" % ( action, package ), 1 )
    utils.debug( "emerge doExec called. action: %s" % action, 2 )
    ret = package.execute( action )
    utils.stopTimer( "%s for %s" % ( action, package ) )
    return ret or continueFlag


def handlePackage( category, packageName, buildAction, continueFlag, skipUpToDateVcs ):
    utils.debug( "emerge handlePackage called: %s %s %s" % (category, packageName, buildAction), 2 )
    success = True
    package = portage.getPackageInstance( category, packageName )
    if package is None:
        raise portage.PortageException( "Package not found", category, packageName )

    if buildAction in [ "all", "full-package", "update", "update-all" ]:
        success = success and doExec( package, "fetch", continueFlag )
        if success and skipUpToDateVcs and package.subinfo.hasSvnTarget( ):
            revision = package.sourceVersion( )
            for p in installdb.getInstalledPackages( category, packageName ):
                if p.getRevision( ) == revision:
                    return True

        success = success and doExec( package, "unpack", continueFlag )
        success = success and doExec( package, "compile" )
        success = success and doExec( package, "cleanimage" )
        success = success and doExec( package, "install" )
        if buildAction in [ "all", "update", "update-all" ]:
            success = success and doExec( package, "qmerge" )
        if buildAction == "full-package":
            success = success and doExec( package, "package" )
        success = success or continueFlag
    elif buildAction in [ "fetch", "unpack", "preconfigure", "configure", "compile", "make", "checkdigest",
                          "dumpdeps", "test",
                          "package", "unmerge", "cleanimage", "cleanbuild", "createpatch",
                          "geturls",
                          "print-revision" ]:
        success = doExec( package, buildAction, continueFlag )
    elif buildAction == "install":
        success = doExec( package, "cleanimage" )
        success = success and doExec( package, "install", continueFlag )
    elif buildAction == "qmerge":
        success = doExec( package, "cleanimage" )
        success = success and doExec( package, "install")
        success = success and doExec( package, "qmerge" )
    elif buildAction == "generate-jenkins-job":
        success = jenkins.generateJob(package)
    elif buildAction == "version-dir":
        print( "%s-%s" % ( packageName, package.sourceVersion( ) ) )
        success = True
    elif buildAction == "version-package":
        print( "%s-%s-%s" % ( packageName, compiler.getCompilerName( ), package.sourceVersion( ) ) )
        success = True
    elif buildAction == "print-targets":
        portage.printTargets( category, packageName )
        success = True
    else:
        success = utils.error( "could not understand this buildAction: %s" % buildAction )

    return success


def handleSinglePackage( packageName, args ):
    _deplist = [ ]
    deplist = [ ]
    packageList = [ ]
    originalPackageList = [ ]
    categoryList = [ ]
    targetDict = dict( )

    if args.action == "update-all":
        installedPackages = portage.PortageInstance.getInstallables( )
        if portage.PortageInstance.isCategory( packageName ):
            utils.debug( "Updating installed packages from category " + packageName, 1 )
        else:
            utils.debug( "Updating all installed packages", 1 )
        packageList = [ ]
        for mainCategory, mainPackage in installedPackages:
            if portage.PortageInstance.isCategory( packageName ) and ( mainCategory != packageName ):
                continue
            if installdb.isInstalled( mainCategory, mainPackage, args.buildType ) \
                    and portage.isPackageUpdateable( mainCategory, mainPackage ):
                categoryList.append( mainCategory )
                packageList.append( mainPackage )
        utils.debug( "Will update packages: " + str( packageList ), 1 )
    elif args.list_file:
        listFileObject = open( args.list_file, 'r' )
        for line in listFileObject:
            if line.strip( ).startswith( '#' ): continue
            try:
                cat, pac, tar, _ = line.split( ',' )
            except:
                continue
            categoryList.append( cat )
            packageList.append( pac )
            originalPackageList.append( pac )
            targetDict[ cat + "/" + pac ] = tar
    elif packageName:
        packageList, categoryList = portage.getPackagesCategories( packageName )

    for entry in packageList:
        utils.debug( "%s" % entry, 1 )
    utils.debug_line( 1 )

    for mainCategory, entry in zip( categoryList, packageList ):
        _deplist = portage.solveDependencies( mainCategory, entry, _deplist, args.dependencyType,
                                              maxDetpth = args.dependencydepth )

    deplist = [ p.ident( ) for p in _deplist ]

    # no package found
    if len( deplist ) == 0:
        category = ""
        if not packageName.find( "/" ) == -1:
            (category, package) = packageName.split( "/" )
        portageSearch.printSearch( category, packageName )
        return False

    for item in deplist:
        item.append( args.ignoreAllInstalled )

        if args.ignoreInstalled and item[ 0 ] in categoryList and item[ 1 ] in packageList or packageIsOutdated(
                item[ 0 ], item[ 1 ] ):
            item[ -1 ] = True

        if item[ 0 ] + "/" + item[ 1 ] in targetDict:
            item[ 3 ] = targetDict[ item[ 0 ] + "/" + item[ 1 ] ]

        if args.target in list(
                portage.PortageInstance.getAllTargets( item[ 0 ], item[ 1 ] ).keys( ) ):
            # if no target or a wrong one is defined, simply set the default target here
            item[ 3 ] = args.target

        utils.debug( "dependency: %s" % item, 1 )


    #for item in deplist:
    #    cat = item[ 0 ]
    #    pac = item[ 1 ]
    #    ver = item[ 2 ]

    #    if portage.isInstalled( cat, pac, ver, buildType) and updateAll and not portage.isPackageUpdateable( cat, pac, ver ):
    #        print "remove:", cat, pac, ver
    #        deplist.remove( item )

    if args.action == "install-deps":
        # the first dependency is the package itself - ignore it
        # TODO: why are we our own dependency?
        del deplist[ 0 ]
    elif args.action == "update-direct-deps":
        for item in deplist:
            item[ -1 ] = True

    deplist.reverse( )

    # package[0] -> category
    # package[1] -> package
    # package[2] -> version

    mainCategory, mainPackage, tag, ignoreInstalled = deplist[ -1 ]
    if not portage.PortageInstance.isVirtualPackage( mainCategory, mainPackage ) and \
        not args.action in [ "all", "install-deps" ,"generate-jenkins-job"] and\
        not args.list_file or\
        args.action in ["print-targets"]:#not all commands should be executed on the deps if we are a virtual packages
        # if a buildAction is given, then do not try to build dependencies
        # and do the action although the package might already be installed.
        # This is still a bit problematic since packageName might not be a valid
        # package
        # for list files, we also want to handle fetching & packaging per package

        if not handlePackage( mainCategory, mainPackage, args.action, args.doContinue, args.update_fast ):
            utils.notify( "Emerge %s failed" % args.action, "%s of %s/%s failed" % (
                args.action, mainCategory, mainPackage), args.action )
            return False
        utils.notify( "Emerge %s finished" % args.action,
                      "%s of %s/%s finished" % ( args.action, mainCategory, mainPackage),
                      args.action )

    else:
        if args.dumpDepsFile:
            dumpDepsFileObject = open( args.dumpDepsFile, 'w+' )
            dumpDepsFileObject.write( "# dependency dump of package %s\n" % ( packageName ) )
        for mainCategory, mainPackage, defaultTarget, ignoreInstalled in deplist:
            isVCSTarget = False

            if args.dumpDepsFile:
                dumpDepsFileObject.write( ",".join( [ mainCategory, mainPackage, defaultTarget, "" ] ) + "\n" )

            isLastPackage = [ mainCategory, mainPackage, defaultTarget, ignoreInstalled ] == deplist[ -1 ]
            if args.outDateVCS or (args.outDatePackage and isLastPackage):
                isVCSTarget = portage.PortageInstance.getUpdatableVCSTargets( mainCategory, mainPackage ) != [ ]
            isInstalled = installdb.isInstalled( mainCategory, mainPackage )
            if args.list_file and args.action != "all":
                ignoreInstalled = mainPackage in originalPackageList
            if ( isInstalled and not ignoreInstalled ) and not (
                            isInstalled and (args.outDateVCS or (
                                    args.outDatePackage and isLastPackage) ) and isVCSTarget ):
                if utils.verbose( ) > 1 and mainPackage == packageName:
                    utils.warning( "already installed %s/%s" % ( mainCategory, mainPackage) )
                elif utils.verbose( ) > 2 and not mainPackage == packageName:
                    utils.warning( "already installed %s/%s" % ( mainCategory, mainPackage ) )
            else:
                # in case we only want to see which packages are still to be build, simply return the package name
                if args.probe:
                    if utils.verbose( ) > 0:
                        msg = " "
                        targetMsg = ":default"
                        if defaultTarget: targetMsg = ":" + defaultTarget
                        utils.warning( "pretending %s/%s%s %s" % ( mainCategory, mainPackage, targetMsg, msg ) )
                else:
                    if args.action in [ "install-deps", "update-direct-deps" ]:
                        args.action = "all"

                    if not handlePackage( mainCategory, mainPackage, args.action, args.doContinue, args.update_fast ):
                        utils.error( "fatal error: package %s/%s %s failed" % \
                                     ( mainCategory, mainPackage, args.action ) )
                        utils.notify( "Emerge build failed",
                                      "Build of %s/%s failed" % ( mainCategory, mainPackage),
                                      args.action )
                        return False
                    utils.notify( "Emerge build finished",
                                  "Build of %s/%s finished" % ( mainCategory, mainPackage),
                                  args.action )

    utils.new_line( )
    return True


def main( ):
    parser = argparse.ArgumentParser( prog = "emerge",
                                      description = "Emerge is a tool for building KDE-related software under Windows. emerge automates it, looks for the dependencies and fetches them automatically.\
                                      Some options should be used with extreme caution since they will make your kde installation unusable in 999 out of 1000 cases.",
                                      epilog = """More information see the README or http://windows.kde.org/.
    Send feedback to <kde-windows@kde.org>.""" )

    def addBuildaAction( x, help = None ):
        parser.add_argument( "--%s" % x, action = "store_const", dest = "action", const = x, default = "all",
                             help = help )

    parser.add_argument( "-p", "--probe", action = "store_true",
                         help = "probing: emerge will only look which files it has to build according to the list of installed files and according to the dependencies of the package." )
    parser.add_argument( "--list-file", action = "store",
                         help = "Build all packages from the csv file provided" )
    parser.add_argument( "--options", action = "append",
                         default = emergeSettings.get( "General", "EMERGE_OPTIONS", "" ).split( ";" ),
                         help = "Set emerge property from string <OPTIONS>. An example for is \"cmake.openIDE=1\" see options.py for more informations." )
    parser.add_argument( "-z", "--outDateVCS", action = "store_true",
                         help = "if packages from version control system sources are installed, it marks them as out of date and rebuilds them (tags are not marked as out of date)." )
    parser.add_argument( "-sz", "--outDatePackage", action = "store_true",
                         help = "similar to -z, only that it acts only on the last package, and works as normal on the rest." )
    parser.add_argument( "-q", "--stayquiet", action = "store_true",
                         dest = "stayQuiet",
                         help = "quiet: there should be no output - The verbose level should be 0" )
    parser.add_argument( "-t", "--buildtests", action = "store_true", dest = "buildTests",
                         default = emergeSettings.getboolean( "General", "EMERGE_BUILDTESTS", False ) )
    parser.add_argument( "-c", "--continue", action = "store_true", dest = "doContinue" )
    parser.add_argument( "--offline", action = "store_true",
                         default = emergeSettings.getboolean( "General", "WorkOffline", False ),
                         help = "do not try to connect to the internet: KDE packages will try to use an existing source tree and other packages would try to use existing packages in the download directory.\
                          If that doesn't work, the build will fail." )
    parser.add_argument( "-f", "--force", action = "store_true", dest = "forced",
                         default = emergeSettings.getboolean( "General", "EMERGE_FORCED", False ) )
    parser.add_argument( "--buildtype", choices = [ "Release", "RelWithDebInfo", "MinSizeRel", "Debug" ],
                         dest = "buildType",
                         default = emergeSettings.get( "General", "EMERGE_BUILDTYPE", "RelWithDebInfo" ),
                         help = "This will override the build type set by the environment option EMERGE_BUILDTYPE ." )
    parser.add_argument( "-v", "--verbose", action = "count",
                         default = int( emergeSettings.get( "EmergeDebug", "Verbose", "1" ) ),
                         help = " verbose: increases the verbose level of emerge. Default is 1. verbose level 1 contains some notes from emerge, all output of cmake, make and other programs that are used.\
                          verbose level 2a dds an option VERBOSE=1 to make and emerge is more verbose highest level is verbose level 3." )
    parser.add_argument( "--trace", action = "store",
                         default = int( emergeSettings.get( "General", "EMERGE_TRACE", "0" ) ), type = int )
    parser.add_argument( "-i", "--ignoreInstalled", action = "store_true",
                         help = "ignore install: using this option will install a package over an existing install. This can be useful if you want to check some new code and your last build isn't that old." )
    parser.add_argument( "-ia", "--ignoreAllInstalled", action = "store_true",
                         help = "ignore all install: using this option will install all package over an existing install. This can be useful if you want to check some new code and your last build isn't that old." )

    parser.add_argument( "--target", action = "store",
                         help = "This will override the build of the default target. The default Target is marked with a star in the printout of --print-targets" )
    parser.add_argument( "--search", action = "store_true",
                         help = "This will search for a package or a description matching or similar to the search term." )
    parser.add_argument( "--nocopy", action = "store_true",
                         default = emergeSettings.getboolean( "General", "EMERGE_NOCOPY", False ),
                         help = "this option is deprecated. In older releases emerge would have copied everything from the SVN source tree to a source directory under KDEROOT\\tmp - currently nocopy is applied\
                          by default if EMERGE_NOCOPY is not set to \"False\". Be aware that setting EMERGE_NOCOPY to \"False\" might slow down the build process, irritate you and increase the disk space roughly\
                           by the size of SVN source tree." )
    parser.add_argument( "--noclean", action = "store_true",
                         default = emergeSettings.getboolean( "General", "EMERGE_NOCLEAN", False ),
                         help = "this option will try to use an existing build directory. Please handle this option with care - it will possibly break if the directory isn't existing." )
    parser.add_argument( "--clean", action = "store_false", dest = "noclean",
                         help = "oposite of --noclean" )
    parser.add_argument( "--patchlevel", action = "store",
                         default = emergeSettings.get( "General", "EMERGE_PKGPATCHLVL", "" ),
                         help = "This will add a patch level when used together with --package" )
    parser.add_argument( "--log-dir", action = "store",
                         default = emergeSettings.get( "General", "EMERGE_LOG_DIR", "" ),
                         help = "This will log the build output to a logfile in LOG_DIR for each package. Logging information is appended to existing logs." )
    parser.add_argument( "--dump-deps-file", action = "store", dest = "dumpDepsFile",
                         help = "Output the dependencies of this package as a csv file suitable for emerge server." )
    parser.add_argument( "--dt", action = "store", choices = [ "both", "runtime", "buildtime" ], default = "both",
                         dest = "dependencyType" )
    parser.add_argument( "--print-installed", action = "store_true",
                         help = "This will show a list of all packages that are installed currently." )
    parser.add_argument( "--print-installable", action = "store_true",
                         help = "his will give you a list of packages that can be installed. Currently you don't need to enter the category and package: only the package will be enough." )
    parser.add_argument( "--update-fast", action = "store_true",
                         help = "If the package is installed from svn/git and the revision did not change all steps after fetch are skipped" )
    parser.add_argument( "-d", "--dependencydepth", action = "store", type = int, default = -1,
                         help = "By default emerge resolves the whole dependency graph, this option limits the depth of the graph, so a value of 1 would mean only dependencies defined in that package" )
    for x in sorted( [ "fetch", "unpack", "preconfigure", "configure", "compile", "make",
                       "install", "qmerge", "manifest", "package", "unmerge", "test",
                       "checkdigest", "dumpdeps",
                       "full-package", "cleanimage", "cleanbuild", "createpatch", "geturls",
                       "version-dir", "version-package", "print-targets",
                       "install-deps" ] ):
        addBuildaAction( x )
    addBuildaAction( "print-revision", "Print the revision of the package and exit" )
    addBuildaAction( "update", "Update a single package" )
    addBuildaAction( "generate-jenkins-job")
    parser.add_argument( "packageNames", nargs = argparse.REMAINDER )

    args = parser.parse_args( )

    if args.stayQuiet == True or args.action in [ "version-dir", "version-package",
                                                  "print-installable", "print-installed",
                                                  "print-targets" ]:
        utils.setVerbose( 0 )
    elif args.verbose:
        utils.setVerbose( args.verbose )

    emergeSettings.set( "General", "WorkOffline", args.offline )
    emergeSettings.set( "General", "EMERGE_NOCOPY", args.nocopy )
    emergeSettings.set( "General", "EMERGE_NOCLEAN", args.noclean )
    emergeSettings.set( "General", "EMERGE_FORCED", args.forced )
    emergeSettings.set( "General", "EMERGE_BUILDTESTS", args.buildTests )
    emergeSettings.set( "General", "EMERGE_BUILDTYPE", args.buildType )
    emergeSettings.set( "PortageVersions", "DefaultTarget", args.target )
    emergeSettings.set( "General", "EMERGE_OPTIONS", ";".join( args.options ) )
    emergeSettings.set( "General", "EMERGE_LOG_DIR", args.log_dir )
    emergeSettings.set( "General", "EMERGE_TRACE", args.trace )
    emergeSettings.set( "General", "EMERGE_PKGPATCHLVL", args.patchlevel )

    if args.search:
        for package in args.packageNames:
            category = ""
            if not package.find( "/" ) == -1:
                (category, package) = package.split( "/" )
            portageSearch.printSearch( category, package )
        return True

    if args.action in [ "install-deps", "update", "update-all" ] or args.update_fast:
        args.ignoreInstalled = True

    if args.action in [ "update", "update-all" ]:
        args.noclean = True

    utils.debug( "buildAction: %s" % args.action )
    utils.debug( "doPretend: %s" % args.probe, 1 )
    utils.debug( "packageName: %s" % args.packageNames )
    utils.debug( "buildType: %s" % args.buildType )
    utils.debug( "buildTests: %s" % args.buildTests )
    utils.debug( "verbose: %d" % utils.verbose( ), 1 )
    utils.debug( "trace: %s" % args.trace, 1 )
    utils.debug( "KDEROOT: %s" % EmergeStandardDirs.emergeRoot( ), 1 )
    utils.debug_line( )

    if args.print_installed:
        printInstalled( )
    elif args.print_installable:
        portage.printInstallables( )
    elif args.list_file:
        handleSinglePackage( "", args )
    else:
        for x in args.packageNames:
            if not handleSinglePackage( x, args ):
                return False
    return True


if __name__ == '__main__':
    succes = True
    try:
        utils.startTimer( "Emerge" )
        doUpdateTitle = True

        def updateTitle( startTime, title ):
            while ( doUpdateTitle ):
                delta = datetime.datetime.now( ) - startTime
                utils.setTitle( "emerge - %s %s" % (title, delta) )
                time.sleep( 1 )

        tittleThread = threading.Thread( target = updateTitle,
                                         args = (datetime.datetime.now( ), " ".join( sys.argv[ 1: ] ),) )
        tittleThread.setDaemon( True )
        tittleThread.start( )
        succes = main( )
    except KeyboardInterrupt:
        pass
    except portage.PortageException as e:
        utils.error( "%s/%s failed: %s" % ( e.category, e.package, e) )
    except Exception as e:
        print( e )
        traceback.print_tb( e.__traceback__ )
    finally:
        utils.stopTimer( "Emerge" )
        doUpdateTitle = False
        if emergeSettings.getboolean( "EmergeDebug", "DumpSettings", False ):
            emergeSettings.dump( )
    if not succes:
        exit( 1 )

