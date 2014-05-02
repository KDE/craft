# -*- coding: utf-8 -*-
# this will emerge some programs...

# copyright:
# Holger Schroeder <holger [AT] holgis [DOT] net>
# Patrick Spendrin <ps_ml [AT] gmx [DOT] de>
# Patrick von Reth <vonreth [AT] kde [DOT] org>

import sys

# The minimum python version for emerge please edit here
# if you add code that changes this requirement
MIN_PY_VERSION = (3, 3, 0)

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
import traceback
from emerge_config import *


@utils.log
def doExec( category, package, action ):
    utils.startTimer( "%s for %s" % ( action, package), 1 )
    utils.debug( "emerge doExec called. action: %s" % action, 2 )
    ret = True
    try:
        #Switched to import the packages only, because otherwise degugging is very hard, if it troubles switch back
        #makes touble for xcompile -> changed back
        pack = portage.getPackageInstance( category, package )
        ret = pack.execute( action )
    except OSError:
        ret =  False
    utils.stopTimer( "%s for %s" % ( action, package) )
    return ret


def updateTitle( startTime, title ):
    while ( True ):
        delta = datetime.datetime.now( ) - startTime
        utils.setTitle( "emerge %s %s" % (title, delta) )
        time.sleep( 1 )


def handlePackage( category, package, version, buildAction, continueFlag ):
    utils.debug( "emerge handlePackage called: %s %s %s %s" % (category, package, version, buildAction), 2 )
    success = True

    if continueFlag:
        actionList = [ 'fetch', 'unpack', 'configure', 'make', 'cleanimage', 'install', 'qmerge' ]

        found = None
        for action in actionList:
            if not found and action != buildAction:
                continue
            found = True
            success = success and doExec( category, package, action )
    elif ( buildAction == "all" or buildAction == "full-package" ):
        success = success and doExec( category, package, "fetch" )
        success = success and doExec( category, package, "unpack" )
        success = success and doExec( category, package, "compile" )
        success = success and doExec( category, package, "cleanimage" )
        success = success and doExec( category, package, "install" )
        if ( buildAction == "all" ):
            success = success and doExec( category, package, "qmerge" )
        if ( buildAction == "full-package" ):
            success = success and doExec( category, package, "package" )

    elif (buildAction in [ "fetch", "unpack", "preconfigure", "configure", "compile", "make", "qmerge", "checkdigest",
                           "dumpdeps",
                           "package", "unmerge", "test", "cleanimage", "cleanbuild", "createpatch",
                           "geturls",
                           "print-revision" ] and category and package and version ):
        success = True
        success = success and doExec( category, package, buildAction )
    elif ( buildAction == "install" ):
        success = True
        success = success and doExec( category, package, "cleanimage" )
        success = success and doExec( category, package, "install" )
    elif ( buildAction == "version-dir" ):
        print( "%s-%s" % ( package, version ) )
        success = True
    elif ( buildAction == "version-package" ):
        print( "%s-%s-%s" % ( package, emergeSettings.get( "General", "KDECOMPILER" ), version ) )
        success = True
    elif ( buildAction == "print-targets" ):
        portage.printTargets( category, package )
        success = True
    else:
        success = utils.error( "could not understand this buildAction: %s" % buildAction )

    return success


def handleSinglePackage( packageName, dependencyDepth ):
    _deplist = [ ]
    deplist = [ ]
    packageList = [ ]
    originalPackageList = [ ]
    categoryList = [ ]
    targetDict = dict( )

    if emergeSettings.args.action == "update-all":
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
                    and portage.isPackageUpdateable( mainCategory, mainPackage ):
                categoryList.append( mainCategory )
                packageList.append( mainPackage )
        utils.debug( "Will update packages: " + str( packageList ), 1 )
    elif emergeSettings.args.list_file:
        listFileObject = open( emergeSettings.args.list_file, 'r' )
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
        _deplist = portage.solveDependencies( mainCategory, entry, "", _deplist, emergeSettings.args.dependencyType,
                                              maxDetpth = dependencyDepth )

    deplist = [ p.ident( ) for p in _deplist ]

    for item in deplist:
        item.append( False )
        if emergeSettings.args.ignoreInstalled and item[ 0 ] in categoryList and item[ 1 ] in packageList:
            item[ -1 ] = True

        if item[ 0 ] + "/" + item[ 1 ] in targetDict:
            item[ 3 ] = targetDict[ item[ 0 ] + "/" + item[ 1 ] ]

        if emergeSettings.args.target in list(
                portage.PortageInstance.getAllTargets( item[ 0 ], item[ 1 ] ).keys( ) ):
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
    elif emergeSettings.args.action == "update-direct-deps":
        for item in deplist:
            item[ -1 ] = True

    deplist.reverse( )

    # package[0] -> category
    # package[1] -> package
    # package[2] -> version

    if ( not emergeSettings.args.action in [ "all", "install-deps", "update-direct-deps" ] and not emergeSettings.args.list_file ):
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
            return False
        utils.notify( "Emerge %s finished" % emergeSettings.args.action,
                      "%s of %s/%s-%s finished" % ( emergeSettings.args.action, mainCategory, mainPackage, mainVersion),
                      emergeSettings.args.action )

    else:
        if emergeSettings.args.dumpDepsFile:
            dumpDepsFileObject = open( emergeSettings.args.dumpDepsFile, 'w+' )
            dumpDepsFileObject.write( "# dependency dump of package %s\n" % ( packageName ) )
        for mainCategory, mainPackage, mainVersion, defaultTarget, ignoreInstalled in deplist:
            isVCSTarget = False

            if emergeSettings.args.dumpDepsFile:
                dumpDepsFileObject.write( ",".join( [ mainCategory, mainPackage, defaultTarget, "" ] ) + "\n" )

            isLastPackage = [ mainCategory, mainPackage, mainVersion, defaultTarget, ignoreInstalled ] == deplist[ -1 ]
            if emergeSettings.args.outDateVCS or (emergeSettings.args.outDatePackage and isLastPackage):
                isVCSTarget = portage.PortageInstance.getUpdatableVCSTargets( mainCategory, mainPackage ) != [ ]
            isInstalled = installdb.isInstalled( mainCategory, mainPackage, mainVersion )
            if emergeSettings.args.list_file and emergeSettings.args.action != "all":
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
                        return False
                    utils.notify( "Emerge build finished",
                                  "Build of %s/%s-%s finished" % ( mainCategory, mainPackage, mainVersion),
                                  emergeSettings.args.action )

    utils.new_line( )
    return True


def main( ):
    utils.startTimer( "Emerge" )
    tittleThread = threading.Thread( target = updateTitle,
                                     args = (datetime.datetime.now( ), " ".join( sys.argv[ 1: ] ),) )
    tittleThread.setDaemon( True )
    tittleThread.start( )



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
        return False

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
    utils.debug( "KDEROOT: %s\n" % emergeRoot(), 1 )
    utils.debug_line( )
    #evenso emerge doesnt depend on the env var KDEROOT anymore there are some scripts that still need it
    utils.putenv("KDEROOT", emergeRoot())



    if emergeSettings.args.print_installed:
        printInstalled( )
    elif emergeSettings.args.print_installable:
        portage.printInstallables( )
    else:
        for x in emergeSettings.args.packageNames:
            if not handleSinglePackage( x, dependencyDepth ):
                return False


if __name__ == '__main__':
    succes = True
    try:
        succes = main( )
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
        traceback.print_tb(e.__traceback__)
    finally:
        utils.stopTimer( "Emerge" )
    if not succes:
        exit(1)