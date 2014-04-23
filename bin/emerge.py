# -*- coding: utf-8 -*-
# this will emerge some programs...

# copyright:
# Holger Schroeder <holger [AT] holgis [DOT] net>
# Patrick Spendrin <ps_ml [AT] gmx [DOT] de>
# Patrick von Reth <vonreth [AT] kde [DOT] org>

import sys

# The minimum python version for emerge please edit here
# if you add code that changes this requirement
MIN_PY_VERSION = (3, 0, 0)

if sys.version_info[ 0:3 ] < MIN_PY_VERSION:
    print( "Error: Python too old!" )
    print( "Emerge needs at least Python Version %s.%s.%s" % MIN_PY_VERSION )
    print( "Please install it and adapt your kdesettings.bat" )
    exit( 1 )

import portageSearch
from InstallDB import *
import time
import datetime
import threading
import argparse
from emerge_config import *


def _exit( code ):
    utils.stopTimer( "Emerge" )
    exit( code )


@utils.log
def doExec( category, package, version, action ):
    utils.startTimer( "%s for %s" % ( action, package), 1 )
    utils.debug( "emerge doExec called. action: %s" % action, 2 )
    fileName = portage.getFilename( category, package, version )

    utils.debug( "file: " + fileName, 1 )
    try:
        #Switched to import the packages only, because otherwise degugging is very hard, if it troubles switch back
        #makes touble for xcompile -> changed back
        mod = portage.__import__( fileName )
        pack = mod.Package( )
        pack.setup( fileName, category, package, version )
        pack.execute( action )
    except OSError:
        utils.stopTimer( "%s for %s" % ( action, package) )
        return False
    utils.stopTimer( "%s for %s" % ( action, package) )
    return True


def updateTitle( startTime, title ):
    while (len( utils._TIMERS ) > 0):
        delta = datetime.datetime.now( ) - startTime
        utils.setTitle( "emerge %s %s" % (title, delta) )
        time.sleep( 1 )


def handlePackage( category, package, version, buildAction, continueFlag ):
    utils.debug( "emerge handlePackage called: %s %s %s %s" % (category, package, version, buildAction), 2 )
    success = True

    if continueFlag:
        actionList = [ 'fetch', 'unpack', 'configure', 'make', 'cleanimage', 'install', 'manifest', 'qmerge' ]

        found = None
        for action in actionList:
            if not found and action != buildAction:
                continue
            found = True
            success = success and doExec( category, package, version, action )
    elif ( buildAction == "all" or buildAction == "full-package" ):
        success = doExec( category, package, version, "fetch" )
        success = success and doExec( category, package, version, "unpack" )
        success = success and doExec( category, package, version, "compile" )
        success = success and doExec( category, package, version, "cleanimage" )
        success = success and doExec( category, package, version, "install" )
        if ( buildAction == "all" ):
            success = success and doExec( category, package, version, "manifest" )
        if ( buildAction == "all" ):
            success = success and doExec( category, package, version, "qmerge" )
        if ( buildAction == "full-package" ):
            success = success and doExec( category, package, version, "package" )

    elif (buildAction in [ "fetch", "unpack", "preconfigure", "configure", "compile", "make", "qmerge", "checkdigest",
                           "dumpdeps",
                           "package", "manifest", "unmerge", "test", "cleanimage", "cleanbuild", "createpatch",
                           "geturls",
                           "print-revision" ] and category and package and version ):
        success = True
        success = success and doExec( category, package, version, buildAction )
    elif ( buildAction == "install" ):
        success = True
        success = success and doExec( category, package, version, "cleanimage" )
        success = success and doExec( category, package, version, "install" )
    elif ( buildAction == "version-dir" ):
        print( "%s-%s" % ( package, version ) )
        success = True
    elif ( buildAction == "version-package" ):
        print( "%s-%s-%s" % ( package, emergeSettings.get( "General", "KDECOMPILER" ), version ) )
        success = True
    elif ( buildAction == "print-installable" ):
        portage.printInstallables( )
        success = True
    elif ( buildAction == "print-installed" ):
        printInstalled( )
        success = True
    elif ( buildAction == "print-targets" ):
        portage.printTargets( category, package, version )
        success = True
    else:
        success = utils.error( "could not understand this buildAction: %s" % buildAction )

    return success


def handleSinglePackage( packageName, dependencyDepth ):
    updateAll = False
    dumpDepsFile = None
    listFile = None
    dependencyType = 'both'

    _deplist = [ ]
    deplist = [ ]
    packageList = [ ]
    originalPackageList = [ ]
    categoryList = [ ]
    targetDict = dict( )

    defaultCategory = emergeSettings.get( "General", "EMERGE_DEFAULTCATEGORY", "kde" )

    if updateAll:
        installedPackages = portage.PortageInstance.getInstallables( )
        if portage.PortageInstance.isCategory( packageName ):
            utils.debug( "Updating installed packages from category " + packageName, 1 )
        else:
            utils.debug( "Updating all installed packages", 1 )
        packageList = [ ]
        for mainCategory, mainPackage, mainVersion in installedPackages:
            if portage.PortageInstance.isCategory( packageName ) and ( mainCategory != packageName ):
                continue
            if installdb.isInstalled( mainCategory, mainPackage, mainVersion, emergeSettings.args.buildType ) \
                    and portage.isPackageUpdateable( mainCategory, mainPackage, mainVersion ):
                categoryList.append( mainCategory )
                packageList.append( mainPackage )
        utils.debug( "Will update packages: " + str( packageList ), 1 )
    elif listFile:
        listFileObject = open( listFile, 'r' )
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
        _deplist = portage.solveDependencies( mainCategory, entry, "", _deplist, dependencyType,
                                              maxDetpth = dependencyDepth )

    deplist = [ p.ident( ) for p in _deplist ]

    for item in deplist:
        item.append( False )
        if emergeSettings.args.ignoreInstalled and item[ 0 ] in categoryList and item[ 1 ] in packageList:
            item[ -1 ] = True

        if item[ 0 ] + "/" + item[ 1 ] in targetDict:
            item[ 3 ] = targetDict[ item[ 0 ] + "/" + item[ 1 ] ]

        if emergeSettings.args.target in list(
                portage.PortageInstance.getAllTargets( item[ 0 ], item[ 1 ], item[ 2 ] ).keys( ) ):
            # if no target or a wrong one is defined, simply set the default target here
            item[ 3 ] = emergeSettings.args.target

        utils.debug( "dependency: %s" % item, 1 )


    #for item in deplist:
    #    cat = item[ 0 ]
    #    pac = item[ 1 ]
    #    ver = item[ 2 ]

    #    if portage.isInstalled( cat, pac, ver, buildType) and updateAll and not portage.isPackageUpdateable( cat, pac, ver ):
    #        print "remove:", cat, pac, ver
    #        deplist.remove( item )

    if emergeSettings.args.action == "install-deps":
        # the first dependency is the package itself - ignore it
        # TODO: why are we our own dependency?
        del deplist[ 0 ]

    if emergeSettings.args.action == "update-direct-deps":
        for item in deplist:
            item[ -1 ] = True

    deplist.reverse( )

    # package[0] -> category
    # package[1] -> package
    # package[2] -> version

    if ( not emergeSettings.args.action in [ "all", "install-deps", "update-direct-deps" ] and not listFile ):
        # if a buildAction is given, then do not try to build dependencies
        # and do the action although the package might already be installed.
        # This is still a bit problematic since packageName might not be a valid
        # package
        # for list files, we also want to handle fetching & packaging per package

        if packageName and len( deplist ) >= 1:
            mainCategory, mainPackage, mainVersion, tag, ignoreInstalled = deplist[ -1 ]
        else:
            mainCategory, mainPackage, mainVersion = None, None, None

        if not handlePackage( mainCategory, mainPackage, mainVersion, emergeSettings.args.action,
                              emergeSettings.args.doContinue ):
            utils.notify( "Emerge %s failed" % emergeSettings.args.action, "%s of %s/%s-%s failed" % (
                emergeSettings.args.action, mainCategory, mainPackage, mainVersion), emergeSettings.args.action )
            _exit( 1 )
        utils.notify( "Emerge %s finished" % emergeSettings.args.action,
                      "%s of %s/%s-%s finished" % ( emergeSettings.args.action, mainCategory, mainPackage, mainVersion),
                      emergeSettings.args.action )

    else:
        if dumpDepsFile:
            dumpDepsFileObject = open( dumpDepsFile, 'w+' )
            dumpDepsFileObject.write( "# dependency dump of package %s\n" % ( packageName ) )
        for mainCategory, mainPackage, mainVersion, defaultTarget, ignoreInstalled in deplist:
            isVCSTarget = False

            if dumpDepsFile:
                dumpDepsFileObject.write( ",".join( [ mainCategory, mainPackage, defaultTarget, "" ] ) + "\n" )

            isLastPackage = [ mainCategory, mainPackage, mainVersion, defaultTarget, ignoreInstalled ] == deplist[ -1 ]
            if emergeSettings.args.outDateVCS or (emergeSettings.args.outDatePackage and isLastPackage):
                isVCSTarget = portage.PortageInstance.getUpdatableVCSTargets( mainCategory, mainPackage,
                                                                              mainVersion ) != [ ]
            isInstalled = installdb.isInstalled( mainCategory, mainPackage, mainVersion, "" )
            if listFile and emergeSettings.args.action != "all":
                ignoreInstalled = mainPackage in originalPackageList
            if ( isInstalled and not ignoreInstalled ) and not (
                            isInstalled and (emergeSettings.args.outDateVCS or (
                                    emergeSettings.args.outDatePackage and isLastPackage) ) and isVCSTarget ):
                if utils.verbose( ) > 1 and mainPackage == packageName:
                    utils.warning( "already installed %s/%s-%s" % ( mainCategory, mainPackage, mainVersion ) )
                elif utils.verbose( ) > 2 and not mainPackage == packageName:
                    utils.warning( "already installed %s/%s-%s" % ( mainCategory, mainPackage, mainVersion ) )
            else:
                # in case we only want to see which packages are still to be build, simply return the package name
                if emergeSettings.args.probe:
                    if utils.verbose( ) > 0:
                        msg = " "
                        targetMsg = ":default"
                        if defaultTarget: targetMsg = ":" + defaultTarget
                        utils.warning( "pretending %s/%s%s %s" % ( mainCategory, mainPackage, targetMsg, msg ) )
                else:
                    if emergeSettings.args.action in [ "install-deps", "update-direct-deps" ]:
                        emergeSettings.args.action = "all"

                    if not handlePackage( mainCategory, mainPackage, mainVersion, emergeSettings.args.action,
                                          emergeSettings.args.doContinue ):
                        utils.error( "fatal error: package %s/%s-%s %s failed" % \
                                     ( mainCategory, mainPackage, mainVersion, emergeSettings.args.action ) )
                        utils.notify( "Emerge build failed",
                                      "Build of %s/%s-%s failed" % ( mainCategory, mainPackage, mainVersion),
                                      emergeSettings.args.action )
                        _exit( 1 )
                    utils.notify( "Emerge build finished",
                                  "Build of %s/%s-%s finished" % ( mainCategory, mainPackage, mainVersion),
                                  emergeSettings.args.action )

    utils.new_line( )


def main( ):
    utils.startTimer( "Emerge" )
    tittleThread = threading.Thread( target = updateTitle,
                                     args = (datetime.datetime.now( ), " ".join( sys.argv[ 1: ] ),) )
    tittleThread.setDaemon( True )
    tittleThread.start( )

    parser = argparse.ArgumentParser( prog = "Emerge",
                                      description = "Emerge is a tool for building KDE-related software under Windows. emerge automates it, looks for the dependencies and fetches them automatically.\
                                      Some options should be used with extreme caution since they will make your kde installation unusable in 999 out of 1000 cases.",
                                      epilog = """More information see the README or http://windows.kde.org/.
    Send feedback to <kde-windows@kde.org>.""" )
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
                         default = utils.varAsBool( emergeSettings.get( "General", "EMERGE_BUILDTESTS", "False" ) ) )
    parser.add_argument( "-c", "--continue", action = "store_true", dest = "doContinue" )
    parser.add_argument( "--offline", action = "store_true",
                         default = utils.varAsBool( emergeSettings.get( "General", "EMERGE_OFFLINE", "False" ) ),
                         help = "do not try to connect to the internet: KDE packages will try to use an existing source tree and other packages would try to use existing packages in the download directory.\
                          If that doesn't work, the build will fail." )
    parser.add_argument( "-f", "--force", action = "store_true", dest = "forced",
                         default = utils.varAsBool( emergeSettings.get( "General", "EMERGE_FORCED", "False" ) ) )
    parser.add_argument( "--buildtype", choices = [ "Release", "RelWithDebInfo", "MinSizeRel" "Debug" ],
                         dest = "buildType",
                         default = emergeSettings.get( "General", "EMERGE_BUILDTYPE", "RelWithDebInfo" ),
                         help = "This will override the build type set by the environment option EMERGE_BUILDTYPE ." )
    parser.add_argument( "-v", "--verbose", action = "count",
                         help = " verbose: increases the verbose level of emerge. Default is 1. verbose level 1 contains some notes from emerge, all output of cmake, make and other programs that are used.\
                          verbose level 2a dds an option VERBOSE=1 to make and emerge is more verbose highest level is verbose level 3." )
    parser.add_argument( "--trace", action = "count", default = emergeSettings.get( "General", "EMERGE_TRACE", "0" ) )
    parser.add_argument( "-i", "--ignoreInstalled", action = "store_true",
                         help = "ignore install: using this option will install a package over an existing install. This can be useful if you want to check some new code and your last build isn't that old." )
    parser.add_argument( "--target", action = "store",
                         help = "This will override the build of the default target. The default Target is marked with a star in the printout of --print-targets" )
    parser.add_argument( "--search", action = "store_true",
                         help = "This will search for a package or a description matching or similar to the search term." )
    parser.add_argument( "--nocopy", action = "store_true",
                         default = utils.varAsBool( emergeSettings.get( "General", "EMERGE_NOCOPY", "False" ) ),
                         help = "this option is deprecated. In older releases emerge would have copied everything from the SVN source tree to a source directory under KDEROOT\\tmp - currently nocopy is applied\
                          by default if EMERGE_NOCOPY is not set to \"False\". Be aware that setting EMERGE_NOCOPY to \"False\" might slow down the build process, irritate you and increase the disk space roughly\
                           by the size of SVN source tree." )
    parser.add_argument( "--noclean", action = "store_true",
                         default = utils.varAsBool( emergeSettings.get( "General", "EMERGE_NOCLEAN", "False" ) ),
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
    for x in sorted( [ "fetch", "unpack", "preconfigure", "configure", "compile", "make",
                                             "install", "qmerge", "manifest", "package", "unmerge", "test",
                                             "checkdigest", "dumpdeps",
                                             "full-package", "cleanimage", "cleanbuild", "createpatch", "geturls",
                                             "version-dir", "version-package", "print-installable",
                                             "print-installed", "print-revision", "print-targets",
                                             "install-deps", "update", "update-direct-deps" ]):
        parser.add_argument( "--%s" % x, action = "store_const" , dest = "action", const = x, default = "all" )
    parser.add_argument( "packageNames", nargs = argparse.REMAINDER )

    emergeSettings.args = parser.parse_args( )
    print( emergeSettings.args )


    if emergeSettings.args.stayQuiet == True or emergeSettings.args.action in [ "version-dir", "version-package",
                                                                                "print-installable", "print-installed",
                                                                                "print-targets" ]:
        utils.setVerbose( 0 )
    elif emergeSettings.args.verbose:
        utils.setVerbose( emergeSettings.args.verbose )

    if emergeSettings.args.search:
        for package in emergeSettings.args.packageNames:
            category = ""
            if not package.find( "/" ) == -1:
                (category, package) = package.split( "/" )
            portageSearch.printSearch( category, package )
        _exit( 0 )

    if emergeSettings.args.action in [ "install-deps", "update", "update-all", "update-direct-deps" ]:
        emergeSettings.args.ignoreInstalled = True

    if emergeSettings.args.action in [ "update", "update-all" ]:
        emergeSettings.args.noclean = True

    dependencyDepth = -1  #TODO

    if emergeSettings.args.action == "update-direct-deps":
        emergeSettings.args.outDateVCS = True
        dependencyDepth = 1

    utils.debug( "buildAction: %s" % emergeSettings.args.action )
    utils.debug( "doPretend: %s" % emergeSettings.args.probe, 1 )
    utils.debug( "packageName: %s" % emergeSettings.args.packageNames )
    utils.debug( "buildType: %s" % emergeSettings.args.buildType )
    utils.debug( "buildTests: %s" % emergeSettings.args.buildTests )
    utils.debug( "verbose: %d" % utils.verbose( ), 1 )
    utils.debug( "trace: %s" % emergeSettings.args.trace, 1 )
    utils.debug( "KDEROOT: %s\n" % emergeSettings.get( "Paths", "KDEROOT" ), 1 )
    utils.debug_line( )

    for x in emergeSettings.args.packageNames:
        handleSinglePackage( x, dependencyDepth )


if __name__ == '__main__':
    main( )