# this will emerge some programs...

# call this with "emerge.py <packageName> <action>"
# where packageName is the program you want to install
# and action is the action you want to do, see base.py
#
# copyright:
# Holger Schroeder <holger [AT] holgis [DOT] net>
# Patrick Spendrin <ps_ml [AT] gmx [DOT] de>

# syntax:
# emerge <options> <action> <packageName>
#
# action can be:
# --fetch, --unpack, --compile, --install, --qmerge
#
# options can be:
# -p for pretend

import sys
import os
import utils

def usage():
    print
    print 'Usage: emerge [-f|-p|-q|-v|--offline][--compile|--fetch|--full-package|'
    print '               --install|--manifest|--package|--print-targets|--qmerge|'
    print '               --unmerge|--unpack] PACKAGES'
    print '       emerge [--print-installable|--print-installed]'
    print 'emerge.py is a script for easier building.'
    print
    print 'Flags:'
    print '-p               pretend to do everything - a dry run'
    print '-q               suppress all output'
    print '-f               force removal of files with unmerge'
    print '-v               print additional output (increase the verbosity level)'
    print '--offline        don\'t try to download anything'
    print '--buildtype=[KdeBuildType] where KdeBuildType is one of the used BuildTypes'
    print '                 This will automatically overrun all buildtype definitions'
    print '                 made in the package\'s .py-file'
    print 'Options:'
    print '--compile PACKAGE       configure and build the PACKAGE'
    print '--fetch PACKAGE         just fetch the PACKAGE'
    print '--full-package PACKAGE  make all of the above steps'
    print '--install PACKAGE       install the PACKAGE to an image directory'
    print '--manifest PACKAGE      add the installdb files to the image directory'
    print '--package PACKAGE       package the image directory with the kdewin-packager[*]'
    print '--print-installable     displays packages that can be installed'
    print '--print-installed       displays installed packages'
    print '--print-targets PACKAGE displays targets for PACKAGE'
    print '--qmerge PACKAGE        install the image directories contents to the kderoot'
    print '--unmerge PACKAGE       try to unmerge PACKAGE'
    print '--unpack PACKAGE        unpack the PACKAGE and apply the patches if needed'
    print '--update PACKAGE        update the PACKAGE if it is installed already; ignored if not present'
    print
    print '[*] - this requires the packager to be installed already.'
    print 'Please see http://windows.kde.org for more information.'
    print 'Send bugs and feature requests to <kde-windows@kde.org>.'
    print

def doExec( category, package, version, action, opts ):
    if utils.verbose() > 2:
        print "emerge doExec called. action: %s opts: %s" % (action, opts)
    fileName = os.path.join( utils.getPortageDir(), category, package, "%s-%s.py" % \
                         ( package, version ) )
    opts_string = ( "%s " * len( opts ) ) % tuple( opts )
    commandstring = "python %s %s %s" % ( fileName, action, opts_string )
    if utils.verbose() > 1:
        print "file:", fileName
        print "commandstring", commandstring
    try:
        utils.system( commandstring ) or utils.die( "running %s" % commandstring )
    except:
        return False
    return True

def handlePackage( category, package, version, buildAction, opts ):
    if utils.verbose() > 1:
        print "emerge handlePackage called: %s %s %s %s" % (category, package, version, buildAction)

    if ( buildAction == "all" or buildAction == "full-package" ):
        success = doExec( category, package, version, "fetch", opts )
        success = success and doExec( category, package, version, "unpack", opts )
        success = success and doExec( category, package, version, "compile", opts )
        success = success and doExec( category, package, version, "cleanimage", opts )
        success = success and doExec( category, package, version, "install", opts )
        if ( buildAction == "all" ):
            success = success and doExec( category, package, version, "manifest", opts )
        if ( buildAction == "all" ):
            success = success and doExec( category, package, version, "qmerge", opts )
        if( buildAction == "full-package" ):
            success = success and doExec( category, package, version, "package", opts )

    elif ( buildAction in [ "fetch", "unpack", "compile", "configure", "make", "qmerge", "package", "manifest", "unmerge" ] ):
        success = doExec( category, package, version, buildAction, opts )
    elif ( buildAction == "install" ):
        success = doExec( category, package, version, "cleanimage", opts )
        success = success and doExec( category, package, version, "install", opts )
    elif ( buildAction == "version-dir" ):
        print "%s-%s" % ( package, version )
        success = True
    elif ( buildAction == "version-package" ):
        print "%s-%s-%s" % ( package, os.getenv( "KDECOMPILER" ), version )
        success = True
    elif ( buildAction == "print-installable" ):
        utils.printInstallables()
        success = True
    elif ( buildAction == "print-installed" ):
        utils.printInstalled()
        success = True
    elif ( buildAction == "print-targets" ):
        utils.printTargets( category, package, version )
        success = True
    else:
        success = utils.error( "could not understand this buildAction: %s" % buildAction )

    return success

buildAction = "all"
packageName = None
doPretend = False
stayQuiet = False
ignoreInstalled = False
opts = ""
environ = dict()
if len( sys.argv ) < 2:
    usage()
    utils.die("")

environ["EMERGE_NOCOPY"]        = os.getenv( "EMERGE_NOCOPY" )
environ["EMERGE_NOUPDATE"]      = os.getenv( "EMERGE_NOUPDATE" )
environ["EMERGE_NOCLEAN"]       = os.getenv( "EMERGE_NOCLEAN" )
environ["EMERGE_VERBOSE"]       = os.getenv( "EMERGE_VERBOSE" )
environ["EMERGE_BUILDTESTS"]    = os.getenv( "EMERGE_BUILDTESTS" )
environ["EMERGE_OFFLINE"]       = os.getenv( "EMERGE_OFFLINE" )
environ["EMERGE_FORCED"]        = os.getenv( "EMERGE_FORCED" )
environ["EMERGE_VERSION"]       = os.getenv( "EMERGE_VERSION" )
environ["EMERGE_BUILDTYPE"]     = os.getenv( "EMERGE_BUILDTYPE" )
environ["EMERGE_TARGET"]        = os.getenv( "EMERGE_TARGET" )

if ( environ['EMERGE_NOCOPY'] == "True" ):
    nocopy = True
else:
    nocopy = False

if ( environ['EMERGE_NOUPDATE'] == "True" ):
    noupdate = True
else:
    noupdate = False

if environ['EMERGE_VERBOSE'] == None or not environ['EMERGE_VERBOSE'].isdigit():
    verbose = 1
    os.environ["EMERGE_VERBOSE"] = str( verbose )
else:
    verbose = int( environ[ "EMERGE_VERBOSE" ] )
    
opts = list()

executableName = sys.argv.pop( 0 )
for i in sys.argv:
    if ( i == "-p" ):
        doPretend = True
    elif ( i == "-q" ):
        stayQuiet = True
    elif ( i == "-t" ):
        os.environ["EMERGE_BUILDTESTS"] = "True"
    elif ( i == "--offline" ):
        opts.append( "--offline" )
        os.environ["EMERGE_OFFLINE"] = "True"
    elif ( i == "-f" ):
        os.environ["EMERGE_FORCED"] = "True"
    elif ( i.startswith( "--version=" ) ):
        os.environ["EMERGE_VERSION"]   = i.replace( "--version=", "" )
    elif ( i.startswith( "--buildtype=" ) ):
        os.environ["EMERGE_BUILDTYPE"] = i.replace( "--buildtype=", "" )
    elif ( i.startswith( "--target=" ) ):
        os.environ["EMERGE_TARGET"] = i.replace( "--target=", "" )
    elif ( i == "-v" ):
        verbose = verbose + 1
        os.environ["EMERGE_VERBOSE"] = str( verbose )
    elif ( i == "--nocopy" ):
        os.environ["EMERGE_NOCOPY"] = str( True )
    elif ( i == "--noclean" ):
        os.environ["EMERGE_NOCLEAN"] = str( True )
    elif ( i == "--clean" ):
        os.environ["EMERGE_NOCLEAN"] = str( False )
    elif ( i in [ "--version-dir", "--version-package", "--print-installable",
                  "--print-installed", "--print-targets" ] ):
        buildAction = i[2:]
        stayQuiet = True
        if i in [ "--print-installable", "--print-installed" ]:
            break
    elif ( i == "-i" ):
        ignoreInstalled = True
    elif ( i == "--update" ):
        ignoreInstalled = True
        os.environ["EMERGE_NOCLEAN"] = str( True )
    elif ( i in [ "--fetch", "--unpack", "--compile", "--configure", "--make",
                  "--install", "--qmerge", "--manifest", "--package", "--unmerge",
                  "--full-package" ] ):
        buildAction = i[2:]
    elif ( i.startswith( "-" ) ):
        usage()
        exit ( 1 )
    else:
        packageName = i
        break

nextArguments = sys.argv[ (sys.argv.index( i ) + 1): ]

if stayQuiet == True:
    verbose = 0
    os.environ["EMERGE_VERBOSE"] = str( verbose )

# get KDEROOT from env
KDEROOT = os.getenv( "KDEROOT" )

if utils.verbose() >= 1:
    print "buildAction:", buildAction
    print "doPretend:", doPretend
    print "packageName:", packageName
    print "buildType:", os.getenv( "EMERGE_BUILDTYPE" )
    print "buildTests:", os.getenv( "EMERGE_BUILDTESTS" )
    print "verbose:", os.getenv( "EMERGE_VERBOSE" )
    print "KDEROOT:", KDEROOT
    
if not os.getenv( "CMAKE_INCLUDE_PATH" ) == None:
    print
    utils.warning( "CMAKE_INCLUDE_PATH found as environment variable. you cannot override emerge"\
                   " with this - unsetting CMAKE_INCLUDE_PATH locally" )
    os.environ["CMAKE_INCLUDE_PATH"]=""

if not os.getenv( "CMAKE_LIBRARY_PATH" ) == None:
    print
    utils.warning( "CMAKE_LIBRARY_PATH found as environment variable. you cannot override emerge"\
                   " with this - unsetting CMAKE_LIBRARY_PATH locally" )
    os.environ["CMAKE_LIBRARY_PATH"]=""

if not os.getenv( "CMAKE_FIND_PREFIX" ) == None:
    print
    utils.warning( "CMAKE_FIND_PREFIX found as environment variable. you cannot override emerge"\
                   " with this - unsetting CMAKE_FIND_PREFIX locally" )
    os.environ["CMAKE_FIND_PREFIX"]=""
    

# adding emerge/bin to find base.py and gnuwin32.py etc.
os.environ["PYTHONPATH"] = os.getenv( "PYTHONPATH" ) + ";" +\
                           os.path.join( os.getcwd(), os.path.dirname( executableName ) )
sys.path.append( os.path.join( os.getcwd(), os.path.dirname( executableName ) ) )

deplist = []

if packageName:
    utils.solveDependencies( "", packageName, "", deplist )
    
if utils.verbose() > 2:
    print "deplist:", deplist

deplist.reverse()

success = True

# package[0] -> category
# package[1] -> package
# package[2] -> version

if ( buildAction != "all" ):
    """if a buildAction is given, then do not try to build dependencies"""
    """and do the action although the package might already be installed"""
    if packageName:
        package = deplist[ -1 ]
    else:
        package = [ None, None, None ]
    ok = handlePackage( package[ 0 ], package[ 1 ], package[ 2 ], buildAction, opts )
else:
    for package in deplist:
        ignore = False
        if package == deplist[ -1 ] and ignoreInstalled:
            ignore = True
        if ( utils.isInstalled( package[0], package[1], package[2] ) and not ignore ):
            if utils.verbose() > 1 and package[1] == packageName:
                utils.warning( "already installed %s/%s-%s" % ( package[0], package[1], package[2] ) )
            elif utils.verbose() > 2 and not package[1] == packageName:
                utils.warning( "already installed %s/%s-%s" % ( package[0], package[1], package[2] ) )
        else:
            if ( doPretend ):
                if utils.verbose() > 0:
                    utils.warning( "pretending %s/%s-%s" % ( package[0], package[1], package[2] ) )
            else:
                if not handlePackage( package[0], package[1], package[2], buildAction, opts ):
                    utils.error( "fatal error: package %s/%s-%s %s failed" % \
                        (package[0], package[1], package[2], buildAction) )

print                        
if len( nextArguments ) > 0:
    command = "emerge.py " + " ".join( nextArguments )
    if utils.verbose() > 1:
        print command

    for element in environ.keys():
        if environ[ element ]:
            os.environ[ element ] = environ[ element ]
        elif element == "EMERGE_VERBOSE":
            os.environ[ element ] = "1"
        else:
            os.environ[ element ] = ""
    utils.system( command ) or utils.die( "cannot execute next commands cmd: %s" % command )
