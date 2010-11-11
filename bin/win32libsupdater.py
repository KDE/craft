# win32libsupdater.py

import os;
import sys;
import imp;
import __builtin__;
import utils;
import portage;
import info;
import subprocess;
from string import Template;

if len( sys.argv ) < 2:
    print "packageList as first argument required!"
    exit( 1 )

# parse the package file
packagefile = file( sys.argv[ 1 ] )
addInfo = dict()
for line in packagefile:
    if not line.startswith( '#' ):
        cat, pac, target, patchlvl = line.strip().split( ',' )
        addInfo[ cat + "/" + pac ] = ( target, patchlvl )
packagefile.close()

baseDependencies = """
    def setDependencies( self ):
        if not os.getenv( 'EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES' ):
            self.buildDependencies[ 'gnuwin32/wget' ] = 'default'
"""

for packageKey in addInfo:
    category, package = packageKey.split( '/' )
    version = portage.PortageInstance.getNewestVersion( category, package )
    srcTargets = portage.PortageInstance.getAllTargets( category, package, version )
    binCategory, binPackage = portage.PortageInstance.getCorrespondingBinaryPackage( package )
    if binPackage:
        utils.debug( "found a binary package for %s" % package, 1 )
        binVersion = portage.PortageInstance.getNewestVersion( binCategory, binPackage )
        binTargets = portage.PortageInstance.getAllTargets( binCategory, binPackage, binVersion )
        
        # check that the target from the source package which has been build is contained in the
        # binary package
        buildTarget = addInfo[ packageKey ] [ 0 ]
        if buildTarget == '':
            buildTarget = portage.PortageInstance.getDefaultTarget( category, package, version )
        regenerateFile = False
        if not buildTarget in binTargets:
            utils.warning( "key %s not contained in binary package %s" % ( buildTarget, binPackage ) )
            regenerateFile = True
        
        dependencies = baseDependencies
        # get buildDependencies from the source package
        runtimeDependencies, buildDependencies = portage.readChildren( category, package, version )
        binRuntimeDependencies, binBuildDependencies = portage.readChildren( binCategory, binPackage, binVersion )
        commonDependencies = dict()

        for i in runtimeDependencies:
            if i in runtimeDependencies and i in buildDependencies:
                commonDependencies[ i ] = buildDependencies[ i ]
                if not i in binRuntimeDependencies:
                    regenerateFile = True

        for key in commonDependencies:
            dependencies += "        self.runtimeDependencies[ '%s' ] = '%s'\n" % ( key, commonDependencies[ key ] )


        if regenerateFile:
            template = Template( file( 'C:/kde/kde-msvc/emerge/bin/binaryPackage.py.template' ).read() )
            targetkeys = binTargets.keys()
            if 'svnHEAD' in binTargets and binTargets['svnHEAD'] == False:
                targetkeys.remove( 'svnHEAD' )
            targetkeys.append( buildTarget )
            targetsString = "'" + "', '".join( targetkeys ) + "'"
            result = template.safe_substitute( { 'revision': '1', 
                                                 'package': binPackage, 
                                                 'versionTargets': targetsString,
                                                 'defaultTarget': buildTarget,
                                                 'dependencies': dependencies
                                               } )

            currentName = portage.getFilename( binCategory, binPackage, binVersion )
            newName = portage.getFilename( binCategory, binPackage, buildTarget )
        
            if not currentName == newName:
                cmd = "svn --non-interactive rename %s %s" % ( currentName, newName )

                utils.debug( "running command: %s" % cmd )
                p = subprocess.Popen( cmd, shell=True, stdin=subprocess.PIPE )
                ret = p.wait()
                
                if not ret == 0:
                    utils.warning( 'failed to rename file %s' % os.path.basename( currentName ) )
                    continue
            
            f = file( newName, 'w+b' )
            f.write( result )
            f.close()
            

        # check that all targets from the source package are contained in the binTargets
        # do we really need binaries for each and every target?
#        utils.new_line
#        for srcKey in srcTargets:
#            if not srcKey in binTargets:
#                utils.warning( "key %s not contained in binary package %s" % ( srcKey, binPackage ) )
#        utils.new_line()
        utils.info( "working on package %s" % package )
        utils.new_line()
    else:
        utils.warning( "no corresponding binary Package is available!" )