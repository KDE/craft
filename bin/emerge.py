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

if sys.version_info[0:3] < MIN_PY_VERSION:
    print ("Error: Python too old!")
    print ("Emerge needs at least Python Version %s.%s.%s" % MIN_PY_VERSION )
    print ("Please install it and adapt your kdesettings.bat")
    exit(1)

import os
import utils
import portage
import emergePlatform
import portageSearch
import shutil
from InstallDB import *
import time
import datetime
import threading
import argparse

def _exit(code):
    utils.stopTimer("Emerge")
    exit(code)



@utils.log
def doExec( category, package, version, action ):
    utils.startTimer("%s for %s" % ( action,package),1)
    utils.debug( "emerge doExec called. action: %s" % action, 2 )
    fileName = portage.getFilename( category, package, version )

    utils.debug( "file: " + fileName, 1 )
    try:
        #Switched to import the packages only, because otherwise degugging is very hard, if it troubles switch back
        #makes touble for xcompile -> changed back
        mod = portage.__import__( fileName )
        pack = mod.Package()
        pack.setup(fileName, category, package, version)
        pack.execute(action)
    except OSError:
        utils.stopTimer("%s for %s" % ( action,package))
        return False
    utils.stopTimer("%s for %s" % ( action,package))
    return True

def updateTitle(startTime,title): 
    while(len(utils._TIMERS)>0):    
        delta = datetime.datetime.now() - startTime
        utils.setTitle("emerge %s %s" %(title , delta))
        time.sleep(1)

def handlePackage( category, package, version, buildAction, continueFlag ):
    utils.debug( "emerge handlePackage called: %s %s %s %s" % (category, package, version, buildAction), 2 )
    success = True

    if continueFlag:
        actionList = ['fetch', 'unpack', 'configure', 'make', 'cleanimage', 'install', 'manifest', 'qmerge']
        
        found = None
        for action in actionList: 
            if not found and action != buildAction:
                continue
            found = True
            success = success and doExec( category, package, version, action )
    elif ( buildAction == "all" or buildAction == "full-package" ):
        os.putenv( "EMERGE_BUILD_STEP", "" )
        success = doExec( category, package, version, "fetch" )
        success = success and doExec( category, package, version, "unpack" )
        if emergePlatform.isCrossCompilingEnabled():
            if not disableHostBuild:
                os.putenv( "EMERGE_BUILD_STEP", "host" )
                success = success and doExec( category, package, version, "compile" )
                success = success and doExec( category, package, version, "cleanimage" )
                success = success and doExec( category, package, version, "install" )
                if ( buildAction == "all" ):
                    success = success and doExec( category, package, version, "manifest" )
                if ( buildAction == "all" ):
                    success = success and doExec( category, package, version, "qmerge" )
                if( buildAction == "full-package" ):
                    success = success and doExec( category, package, version, "package" )
            if disableTargetBuild:
                return success
            os.putenv( "EMERGE_BUILD_STEP", "target" )

        success = success and doExec( category, package, version, "compile" )
        success = success and doExec( category, package, version, "cleanimage" )
        success = success and doExec( category, package, version, "install" )
        if ( buildAction == "all" ):
            success = success and doExec( category, package, version, "manifest" )
        if ( buildAction == "all" ):
            success = success and doExec( category, package, version, "qmerge" )
        if( buildAction == "full-package" ):
            success = success and doExec( category, package, version, "package" )

    elif ( buildAction in [ "fetch", "unpack", "preconfigure", "configure", "compile", "make", "qmerge", "checkdigest", "dumpdeps",
                            "package", "manifest", "unmerge", "test", "cleanimage", "cleanbuild", "createpatch", "geturls",
                            "printrev"] and category and package and version ):
        os.putenv( "EMERGE_BUILD_STEP", "" )
        success = True
        if emergePlatform.isCrossCompilingEnabled():
            if not disableHostBuild:
                os.putenv( "EMERGE_BUILD_STEP", "host" )
                success = doExec( category, package, version, buildAction )
            if disableTargetBuild:
                return success
            os.putenv( "EMERGE_BUILD_STEP", "target" )
        success = success and doExec( category, package, version, buildAction )
    elif ( buildAction == "install" ):
        os.putenv( "EMERGE_BUILD_STEP", "" )
        success = True
        if emergePlatform.isCrossCompilingEnabled():
            if not disableHostBuild:
                os.putenv( "EMERGE_BUILD_STEP", "host" )
                success = doExec( category, package, version, "cleanimage" )
                success = success and doExec( category, package, version, "install" )
            if disableTargetBuild:
                return success
            os.putenv( "EMERGE_BUILD_STEP", "target" )
        success = success and doExec( category, package, version, "cleanimage" )
        success = success and doExec( category, package, version, "install" )
    elif ( buildAction == "version-dir" ):
        print("%s-%s" % ( package, version ))
        success = True
    elif ( buildAction == "version-package" ):
        print("%s-%s-%s" % ( package, os.getenv( "KDECOMPILER" ), version ))
        success = True
    elif ( buildAction == "print-installable" ):
        portage.printInstallables()
        success = True
    elif ( buildAction == "print-installed" ):
        if isDBEnabled():
            printInstalled()
        else:
            portage.printInstalled()
        success = True
    elif ( buildAction == "print-targets" ):
        portage.printTargets( category, package, version )
        success = True
    else:
        success = utils.error( "could not understand this buildAction: %s" % buildAction )

    return success

#
# "main" action starts here
#

# TODO: all the rest should go into main(). But here I am not
# sure - maybe some of those variables are actually MEANT to
# be used in other modules. Put this back for now

# but as a temporary solution rename variables to mainXXX
# where it is safe so there are less redefinitions in inner scopes

utils.startTimer("Emerge")
tittleThread = threading.Thread(target=updateTitle,args = (datetime.datetime.now()," ".join(sys.argv[1:]),))
tittleThread.setDaemon(True)
tittleThread.start()


if not "EMERGE_TRACE" in os.environ:
    trace = 0
    os.environ["EMERGE_TRACE"] = str( trace )
else:
    trace = int( os.environ[ "EMERGE_TRACE" ] )

parser = argparse.ArgumentParser(prog = "Emerge",
description = "Emerge is a tool for building KDE-related software under Windows. emerge automates it, looks for the dependencies and fetches them automatically. Some options should be used with extreme caution since they will make your kde installation unusable in 999 out of 1000 cases.",
epilog = """More information see the README or http://windows.kde.org/.
Send feedback to <kde-windows@kde.org>.""")
parser.add_argument("-p", "--probe", action = "store_true", help = "probing: emerge will only look which files it has to build according to the list of installed files and according to the dependencies of the package.")
parser.add_argument("--list-file", action = "append" )
    # elif ( i.startswith("--options=") ):
        # # @todo how to add -o <parameter> option
        # options = i.replace( "--options=", "" )
        # if "EMERGE_OPTIONS" in os.environ:
            # os.environ["EMERGE_OPTIONS"] += " %s" % options
        # else:
            # os.environ["EMERGE_OPTIONS"] = options
parser.add_argument("-z","--outDateVCS", action = "store_true", help = "if packages from version control system sources are installed, it marks them as out of date and rebuilds them (tags are not marked as out of date).")
parser.add_argument("-sz","--outDatePackage", action = "store_true", help = "similar to -z, only that it acts only on the last package, and works as normal on the rest.")
parser.add_argument("-q","--stayQuiet", action = "store_true", help = "quiet: there should be no output - The verbose level should be 0")
    # elif ( i == "-t" ):
        # os.environ["EMERGE_BUILDTESTS"] = "True"
parser.add_argument("-c","--continue", action = "store_true", dest = "doContinue")
parser.add_argument("--offline", action = "store_true")
#        os.environ["EMERGE_OFFLINE"] = "True"
parser.add_argument("-f","--force", action = "store_true")
        # os.environ["EMERGE_FORCED"] = "True"
parser.add_argument("--buildtype", choices = ["Release", "RelWithDebInfo", "MinSizeRel" "Debug"], help = "This will override the build type set by the environment option EMERGE_BUILDTYPE .")
        # os.environ["EMERGE_BUILDTYPE"] = i.replace( "--buildtype=", "" )
parser.add_argument("-v","--verbose", action = "count", help = " verbose: increases the verbose level of emerge. Default is 1. verbose level 1 contains some notes from emerge, all output of cmake, make and other programs that are used. verbose level 2a dds an option VERBOSE=1 to make and emerge is more verbose highest level is verbose level 3.")
parser.add_argument("-i","--ignoreInstalled", action = "store_true")
parser.add_argument("-a", "--action", choices = ["fetch", "unpack", "preconfigure", "configure", "compile", "make",
                  "install", "qmerge", "manifest", "package", "unmerge", "test", "checkdigest", "dumpdeps",
                  "full-package", "cleanimage", "cleanbuild", "createpatch", "geturls",
                  "version-dir", "version-package", "print-installable",
                  "print-installed", "print-targets",
                  "install-deps", "update", "update-direct-deps"], default = "all") 
parser.add_argument("--target", action = "store" )
        # os.environ["EMERGE_TARGET"] = i.replace( "--target=", "" )
parser.add_argument("--search", action = "store_true")
        
        
    # elif ( i.startswith( "--patchlevel=" ) ):
        # # os.environ["EMERGE_PKGPATCHLVL"] = i.replace( "--patchlevel=", "" )
    # elif ( i.startswith( "--log-dir=" ) ):
        # os.environ["EMERGE_LOG_DIR"] = i.replace( "--log-dir=", "" )
    # elif ( i.startswith( "--dump-deps-file=" ) ):
        # dumpDepsFile = i.replace( "--dump-deps-file=", "" )
    # elif ( i.startswith( "--dt=" ) ):
        # dependencyType = i.replace( "--dt=", "" )
        # if dependencyType not in ['both', 'runtime', 'buildtime']:
            # dependencyType = 'both'
        
    # elif ( i == "--trace" ):
        # trace = trace + 1
        # os.environ["EMERGE_TRACE"] = str( trace )
    # elif ( i == "--nocopy" ):
        # os.environ["EMERGE_NOCOPY"] = str( True )
    # elif ( i == "--noclean" ):
        # os.environ["EMERGE_NOCLEAN"] = str( True )
    # elif ( i == "--clean" ):
        # os.environ["EMERGE_NOCLEAN"] = str( False )

    # elif ( i == "--update" ):
        # ignoreInstalled = True
        # os.environ["EMERGE_NOCLEAN"] = str( True )
    # elif ( i == "--update-all" ):
        # ignoreInstalled = True
        # os.environ["EMERGE_NOCLEAN"] = str( True )
        # updateAll = True


    # elif ( i == "--print-revision" ):
        # mainBuildAction = "printrev"



parser.add_argument("packageNames", nargs = "*")

args = parser.parse_args()
print(args)

if args.stayQuiet == True or args.action in [ "version-dir", "version-package", "print-installable","print-installed", "print-targets" ]:
    utils.setVerbose(0)
elif args.verbose:
    utils.setVerbose(args.verbose)
   
    


# get KDEROOT from env
KDEROOT = os.getenv( "KDEROOT" )
utils.debug( "buildAction: %s" % args.action )
utils.debug( "doPretend: %s" % args.probe, 1 )
utils.debug( "packageName: %s" % args.packageNames )
utils.debug( "buildType: %s" % os.getenv( "EMERGE_BUILDTYPE" ) )
utils.debug( "buildTests: %s" % utils.envAsBool( "EMERGE_BUILDTESTS" ) )
utils.debug( "verbose: %d" % utils.verbose(), 1 )
utils.debug( "trace: %s" % os.getenv( "EMERGE_TRACE" ), 1 )
utils.debug( "KDEROOT: %s\n" % KDEROOT, 1 )
utils.debug_line()

def mainThing(packageName, dependencyDepth):
    global args
    disableHostBuild = False
    disableTargetBuild = False
    updateAll = False
    dumpDepsFile = None
    listFile = None
    dependencyType = 'both'

    _deplist = []
    deplist = []
    packageList = []
    originalPackageList = []
    categoryList = []
    targetDict = dict()


    buildType = os.getenv("EMERGE_BUILDTYPE")
    if "EMERGE_DEFAULTCATEGORY" in os.environ:
        defaultCategory = os.environ["EMERGE_DEFAULTCATEGORY"]
    else:
        defaultCategory = "kde"

    if updateAll:
        installedPackages = portage.PortageInstance.getInstallables()
        if portage.PortageInstance.isCategory( packageName ):
            utils.debug( "Updating installed packages from category " + packageName, 1 )
        else:
            utils.debug( "Updating all installed packages", 1 )
        packageList = []
        for mainCategory, mainPackage, mainVersion in installedPackages:
            if portage.PortageInstance.isCategory( packageName ) and ( mainCategory != packageName ):
                continue
            if portage.isInstalled( mainCategory, mainPackage, mainVersion, buildType ) \
                    and portage.isPackageUpdateable( mainCategory, mainPackage, mainVersion ):
                categoryList.append( mainCategory )
                packageList.append( mainPackage )
        utils.debug( "Will update packages: " + str (packageList), 1 )
    elif listFile:
        listFileObject = open( listFile, 'r' )
        for line in listFileObject:
            if line.strip().startswith('#'): continue
            try:
                cat, pac, tar, _ = line.split( ',' )
            except:
                continue
            categoryList.append( cat )
            packageList.append( pac )
            originalPackageList.append( pac )
            targetDict[ cat + "/" + pac ] = tar
    elif packageName:
        packageList, categoryList = portage.getPackagesCategories(packageName)

    for entry in packageList:
        utils.debug( "%s" % entry, 1 )
    utils.debug_line( 1 )

    for mainCategory, entry in zip (categoryList, packageList):
        _deplist = portage.solveDependencies( mainCategory, entry, "", _deplist, dependencyType, maxDetpth = dependencyDepth )

    deplist = [p.ident() for p in _deplist]
    target = os.getenv( "EMERGE_TARGET" )


    for item in deplist: 
        item.append( False )
        if args.ignoreInstalled and item[ 0 ] in categoryList and item[ 1 ] in packageList:
            item[-1] =  True
            
        if  item[ 0 ] + "/" + item[ 1 ] in targetDict:
            item[ 3 ] = targetDict[ item[ 0 ] + "/" + item[ 1 ] ]
            
        if target in list( portage.PortageInstance.getAllTargets( item[ 0 ], item[ 1 ], item[ 2 ] ).keys()):
            # if no target or a wrong one is defined, simply set the default target here
            item[ 3 ] = target
            
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
        
    if args.action == "update-direct-deps":
        for item in deplist:
            item[-1] =  True

    deplist.reverse()

    # package[0] -> category
    # package[1] -> package
    # package[2] -> version

    if ( not args.action in ["all", "install-deps", "update-direct-deps"] and not listFile ):
        # if a buildAction is given, then do not try to build dependencies
        # and do the action although the package might already be installed.
        # This is still a bit problematic since packageName might not be a valid
        # package
        # for list files, we also want to handle fetching & packaging per package

        if packageName and len( deplist ) >= 1:
            mainCategory, mainPackage, mainVersion, tag, ignoreInstalled = deplist[ -1 ]
        else:
            mainCategory, mainPackage, mainVersion = None, None, None

        if not handlePackage( mainCategory, mainPackage, mainVersion, args.action, args.doContinue ):
            utils.notify("Emerge %s failed" % args.action, "%s of %s/%s-%s failed" % ( args.action,mainCategory, mainPackage, mainVersion),args.action)
            _exit(1)
        utils.notify("Emerge %s finished"% args.action, "%s of %s/%s-%s finished" % ( args.action,mainCategory, mainPackage, mainVersion),args.action)

    else:
        if dumpDepsFile:
            dumpDepsFileObject = open( dumpDepsFile, 'w+' )
            dumpDepsFileObject.write( "# dependency dump of package %s\n" % ( packageName ) )
        for mainCategory, mainPackage, mainVersion, defaultTarget, ignoreInstalled in deplist:
            isVCSTarget = False

            if dumpDepsFile:
                dumpDepsFileObject.write( ",".join( [ mainCategory, mainPackage, defaultTarget, "" ] ) + "\n" )

            isLastPackage = [mainCategory, mainPackage, mainVersion, defaultTarget, ignoreInstalled] == deplist[-1]
            if args.outDateVCS or (args.outDatePackage and isLastPackage):
                isVCSTarget = portage.PortageInstance.getUpdatableVCSTargets( mainCategory, mainPackage, mainVersion ) != []
            if isDBEnabled():
                if emergePlatform.isCrossCompilingEnabled():
                    hostEnabled = portage.isHostBuildEnabled( mainCategory, mainPackage, mainVersion )
                    targetEnabled = portage.isTargetBuildEnabled( mainCategory, mainPackage, mainVersion )
                    hostInstalled = installdb.isInstalled( mainCategory, mainPackage, mainVersion, "" )
                    targetInstalled = installdb.isInstalled( mainCategory, mainPackage, mainVersion, os.getenv( "EMERGE_TARGET_PLATFORM" ) )
                    isInstalled = ( not hostEnabled or hostInstalled ) and ( not targetEnabled or targetInstalled )
                else:
                    isInstalled = installdb.isInstalled( mainCategory, mainPackage, mainVersion, "" )
            else:
                isInstalled = portage.isInstalled( mainCategory, mainPackage, mainVersion, buildType )
            if listFile and args.action != "all":
                ignoreInstalled = mainPackage in originalPackageList
            if ( isInstalled and not ignoreInstalled ) and not (
                            isInstalled and (args.outDateVCS  or (args.outDatePackage and isLastPackage) ) and isVCSTarget ):
                if utils.verbose() > 1 and mainPackage == packageName:
                    utils.warning( "already installed %s/%s-%s" % ( mainCategory, mainPackage, mainVersion ) )
                elif utils.verbose() > 2 and not mainPackage == packageName:
                    utils.warning( "already installed %s/%s-%s" % ( mainCategory, mainPackage, mainVersion ) )
            else:
                # in case we only want to see which packages are still to be build, simply return the package name
                if ( args.probe ):
                    if utils.verbose() > 0:
                        msg = " "
                        if emergePlatform.isCrossCompilingEnabled():
                            if isDBEnabled():
                                hostEnabled = portage.isHostBuildEnabled( mainCategory, mainPackage, mainVersion )
                                targetEnabled = portage.isTargetBuildEnabled( mainCategory, mainPackage, mainVersion )
                                hostInstalled = installdb.isInstalled( mainCategory, mainPackage, mainVersion, "" )
                                targetInstalled = installdb.isInstalled( mainCategory, mainPackage, mainVersion, os.getenv( "EMERGE_TARGET_PLATFORM" ) )
                                msg += portage.getHostAndTarget( hostEnabled and not hostInstalled, targetEnabled and not targetInstalled )
                            else:
                                msg = ""
                        targetMsg = ":default"
                        if defaultTarget: targetMsg = ":" + defaultTarget
                        utils.warning( "pretending %s/%s%s %s" % ( mainCategory, mainPackage, targetMsg, msg ) )
                else:
                    mainAction = args.action
                    if args.action in ["install-deps", "update-direct-deps"]:
                        mainAction = "all"
                        
                    if defaultTarget: os.environ["EMERGE_TARGET"] = defaultTarget

                    if not handlePackage( mainCategory, mainPackage, mainVersion, mainAction, args.doContinue ):
                        utils.error( "fatal error: package %s/%s-%s %s failed" % \
                            ( mainCategory, mainPackage, mainVersion, args.action ) )
                        utils.notify("Emerge build failed", "Build of %s/%s-%s failed" % ( mainCategory, mainPackage, mainVersion),mainAction)
                        _exit( 1 )
                    utils.notify("Emerge build finished", "Build of %s/%s-%s finished" % ( mainCategory, mainPackage, mainVersion),mainAction)

    utils.new_line()


if args.search:
    for package in args.packageNames:
        category = ""
        if not package.find("/") == -1:
            (category,package) = package.split("/")
        portageSearch.printSearch(category, package)
    _exit(0)

if args.action in ["install-deps", "update", "update-all", "update-direct-deps"]:
    args.ignoreInstalled = True

#todo
# if args.action in ["update", "update-all"]:
    # os.environ["EMERGE_NOCLEAN"] = str( True )

dependencyDepth = -1 #TODO

if args.action == "update-direct-deps":
        args.outDateVCS = True
        dependencyDepth = 1
        
for x in args.packageNames:
    mainThing(x, dependencyDepth)
