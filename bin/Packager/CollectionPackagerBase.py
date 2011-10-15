#
# copyright (c) 2010-2011 Patrick Spendrin <ps_ml@gmx.de>
# copyright (c) 2010 Andre Heinecke <aheinecke@intevation.de> (code taken from the kdepim-ce-package.py)
#
from Packager.PackagerBase import *
import shutil
import re
import types
import fileinput
from _winreg import * # pylint: disable=F0401
import compiler

class PackagerLists(object):
    """ This class provides some staticmethods that can be used as pre defined black or whitelists """
    @staticmethod
    def runtimeBlacklist():
        blacklisted = [ "include\\.*",
                        "lib\\\\.*\.lib",
                        "lib\\\\.*\.dll\.a",
                        "lib\\\\cmake\\.*",
                        "lib\\\\pkgconfig\\.*" ]
        ret = []
        for line in blacklisted:
            try:
                exp = re.compile( line )
                ret.append( exp )
                utils.debug( "%s added to blacklist as %s" % ( line, exp.pattern ), 2 )
            except re.error:
                utils.debug( "%s is not a valid regexp" % line, 1 )
        return ret

    @staticmethod
    def defaultWhitelist():
        return [ re.compile( ".*" ) ]

    @staticmethod
    def defaultBlacklist():
        return []


class CollectionPackagerBase( PackagerBase ):
    def __init__( self, whitelists=None, blacklists=None):
        PackagerBase.__init__( self )
        if whitelists is None:
            whitelists = [ PackagerLists.defaultWhitelist ]
        if blacklists is None:
            blacklists = [ PackagerLists.defaultBlacklist ]
        self.defines = dict()
        self.whitelist = []
        self.blacklist = []

        for entry in whitelists:
            utils.debug( "reading whitelist: %s" % entry, 2 )
            if isinstance( entry, types.FunctionType ) or isinstance( entry, types.MethodType ):
                for line in entry():
                    self.whitelist.append( line )
            else:
                self.read_whitelist( entry )
        for entry in blacklists:
            utils.debug( "reading blacklist: %s" % entry, 2 )
            if isinstance( entry, types.FunctionType ) or isinstance( entry, types.MethodType ):
                for line in entry():
                    self.blacklist.append( line )
            else:
                self.read_blacklist( entry )
        utils.debug( "length of blacklist: %s" % len( self.blacklist ), 0 )
        utils.debug( "length of whitelist: %s" % len( self.whitelist ), 0 )

        self.scriptname = None

    def __isInstalled( self ):
        return abstract()

    def __imageDirPattern( self, package, buildTarget ):
        """ return base directory name for package related image directory """
        directory = "image"

        # we assume that binary packages are for all compiler and targets
        ## \todo add image directory support for using binary packages for a specific compiler and build type
        if package.buildSystemType == 'binary':
            return directory

        if package.subinfo.options.useCompilerType == True:
            directory += '-' + COMPILER
        if package.isTargetBuild():
            directory += "-%s" % package.buildPlatform()
        if package.subinfo.options.useBuildType == True:
            directory += '-' + package.buildType()
        directory += '-' + buildTarget
        return directory

    def __buildRoot( self, category, package, version ):
        """ return absolute path to the root directory of the currently active package - taken from EmergeBase """
        return os.path.join( self.rootdir, "build", category, "%s-%s" % ( package, version ) )

    def __getImageDirectories( self ):
        """ return the image directories where the files are stored """
        imageDirs = []
        runtimeDependencies = self.subinfo.runtimeDependencies

        commonDependencies = self.subinfo.hardDependencies
        commonDependencies.update( self.subinfo.dependencies )
        for key in commonDependencies:
            runtimeDependencies[ key ] = commonDependencies[ key ]

        depList = []
        for key in runtimeDependencies:
            ( category, package ) = key.split( '/' )
            version = portage.PortageInstance.getNewestVersion( category, package )
            # we only want runtime dependencies since we want to build a binary installer
            portage.solveDependencies( category, package, version, depList, "runtime" )
        depList.reverse()
        for x in depList:
            ( category, package, version, defaultTarget ) = x.ident()
            # Ignore dev-utils that are wrongly set as hard dependencies
            if category == "dev-util":
                continue
            defaultTarget = portage.findPossibleTargets( category, package, version )
            _package = portage.getPackageInstance( category, package, defaultTarget )
            imageDirs.append( ( os.path.join( self.__buildRoot( category, package, version ),
                    self.__imageDirPattern( _package, defaultTarget ) ), _package.subinfo.options.merge.destinationPath , _package.subinfo.options.package.disableStriping ) )
            # this loop collects the files from all image directories
        return imageDirs

    def read_whitelist( self, fname ):
        """ Read regular expressions from fname """
        fname = os.path.join( self.packageDir(), fname )
        if not os.path.isfile( fname ):
            utils.die( "Whitelist not found at: %s" % os.path.abspath( fname ) )
            return False
        for line in fileinput.input( fname ):
            # Cleanup white spaces / line endings
            line = line.splitlines()
            line = line[ 0 ].rstrip()
            if line.startswith( "#" ) or len( line ) == 0:
                continue
            try:
                exp = re.compile( line )
                self.whitelist.append( exp )
                utils.debug( "%s added to whitelist as %s" % ( line, exp.pattern ), 2 )
            except re.error:
                utils.debug( "%s is not a valid regexp" % line, 1 )

    def read_blacklist( self, fname ):
        """ Read regular expressions from fname """
        fname = os.path.join( self.packageDir(), fname )
        if not os.path.isfile( fname ):
            utils.die( "Blacklist not found at: %s" % os.path.abspath( fname ) )
            return False
        for line in fileinput.input( fname ):
            # Cleanup white spaces / line endings
            line = line.splitlines()
            line = line[ 0 ].rstrip()
            if line.startswith( "#" ) or len( line ) == 0:
                continue
            try:
                exp = re.compile( line )
                self.blacklist.append( exp )
                utils.debug( "%s added to blacklist as %s" % ( line, exp.pattern ), 2 )
            except re.error:
                utils.debug( "%s is not a valid regexp" % line, 1 )

    def whitelisted( self, pathname ):
        """ return True if pathname is included in the pattern, and False if not """
        for pattern in self.whitelist:
            if pattern.search( pathname ):
                return True
        return False

    def blacklisted( self, filename ):
        """ return False if file is not blacklisted, and True if it is blacklisted """
        for pattern in self.blacklist:
            if pattern.search( filename ):
                return True
        return False

    def traverse( self, directory, whitelist = lambda f: True, blacklist = lambda g: False ):
        """
            Traverse through a directory tree and return every
            filename that the function whitelist returns as true and
            which do not match blacklist entries
        """
        if blacklist( directory ):
            return
        dirs = [ directory ]
        while dirs:
            path = dirs.pop()
            for f in os.listdir( path ):
                f = os.path.join( path, f )
                z = f.replace( directory + os.sep, "" )
                if blacklist( z ):
                    continue
                if os.path.isdir( f ):
                    dirs.append( f )
                elif os.path.isfile( f ) and whitelist( z ):
                    yield f

    def copyFiles( self, srcDir, destDir, strip  ):
        """
            Copy the binaries for the Package from srcDir to the imageDir
            directory
        """
        utils.createDir( destDir )
        utils.debug( "Copying from %s ..." % ( srcDir ) )
        uniquebasenames = []
        self.unique_names = []
        duplicates = []

        for entry in self.traverse( srcDir, self.whitelisted, self.blacklisted ):
            if os.path.basename( entry ) in uniquebasenames:
                utils.debug( "Found duplicate filename: %s" % os.path.basename( entry ), 2 )
                duplicates.append( entry )
            else:
                self.unique_names.append( entry )
                uniquebasenames.append( os.path.basename( entry ) )

        for entry in self.unique_names:
            entry_target = entry.replace( srcDir, os.path.join( destDir + os.path.sep ) )
            if not os.path.exists( os.path.dirname( entry_target ) ):
                utils.createDir( os.path.dirname( entry_target ) )
            shutil.copy( entry, entry_target )
            utils.debug( "Copied %s to %s" % ( entry, entry_target ), 2 )
            if strip and entry_target.endswith(".dll") or entry_target.endswith(".exe"):
                self.strip( entry_target )
        for entry in duplicates:
            entry_target = entry.replace( srcDir, os.path.join( destDir + os.path.sep ) )
            if not os.path.exists( os.path.dirname( entry_target ) ):
                utils.createDir( os.path.dirname( entry_target ) )
            shutil.copy( entry, entry_target )
            utils.debug( "Copied %s to %s" % ( entry, entry_target ), 2 )
            if strip and entry_target.endswith(".dll") or entry_target.endswith(".exe"):
                self.strip( entry_target )
          
    def internalCreatePackage( self ):
        """ create a package """
        if not utils.envAsBool("EMERGE_NOCLEAN"):
            utils.debug( "cleaning imagedir: %s" % self.imageDir() )
            utils.cleanDirectory( self.imageDir() )
            for directory, mergeDir, strip  in self.__getImageDirectories():
                imageDir = self.imageDir()
                if mergeDir:
                    imageDir = os.path.join( imageDir, mergeDir )
                if os.path.exists( directory ):
                    self.copyFiles(directory, imageDir, strip)
                else:
                    utils.warning( "image directory %s does not exist!" % directory )

        if not os.path.exists( self.imageDir() ):
            os.makedirs( self.imageDir() )

        return True
