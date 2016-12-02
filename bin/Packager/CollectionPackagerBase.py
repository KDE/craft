#
# copyright (c) 2010-2011 Patrick Spendrin <ps_ml@gmx.de>
# copyright (c) 2010 Andre Heinecke <aheinecke@intevation.de> (code taken from the kdepim-ce-package.py)
#
import shutil
import re
import types
import fileinput

from portage import DependencyPackage, DependencyType
import CraftDebug
from Packager.PackagerBase import *


class PackagerLists(object):
    """ This class provides some staticmethods that can be used as pre defined black or whitelists """
    @staticmethod
    def runtimeBlacklist():
        blacklisted = [ "include\\\\.*",
                        "lib\\\\.*\.lib",
                        "lib\\\\.*\.dll\.a",
                        "lib\\\\cmake\\.*",
                        "lib\\\\pkgconfig\\.*" ]
        ret = []
        for line in blacklisted:
            try:
                exp = re.compile( line, re.IGNORECASE )
                ret.append( exp )
                CraftDebug.debug("%s added to blacklist as %s" % (line, exp.pattern), 2)
            except re.error:
                CraftDebug.debug("%s is not a valid regexp" % line, 1)
        return ret

    @staticmethod
    def defaultWhitelist():
        return [ re.compile( ".*" ) ]

    @staticmethod
    def defaultBlacklist():
        return []


class CollectionPackagerBase( PackagerBase ):
    def __init__( self, whitelists=None, blacklists=None, initialized = False):
        if not initialized: PackagerBase.__init__(self)
        if not whitelists:
            whitelists = [ PackagerLists.defaultWhitelist ]
        if not blacklists:
            blacklists = [ PackagerLists.defaultBlacklist ]
        if not self.whitelist_file:
            self.whitelist_file = whitelists
        if not self.blacklist_file:
            self.blacklist_file = blacklists
        self._whitelist = []
        self._blacklist = []

        self.scriptname = None

    @property
    def whitelist(self):
        if not self._whitelist:
            for entry in self.whitelist_file:
                CraftDebug.debug("reading whitelist: %s" % entry, 2)
                if isinstance( entry, types.FunctionType ) or isinstance( entry, types.MethodType ):
                    for line in entry():
                        self._whitelist.append( line )
                else:
                    self.read_whitelist( entry )
        return self._whitelist

    @property
    def blacklist(self):
        if not self._blacklist:
            for entry in self.blacklist_file:
                CraftDebug.debug("reading blacklist: %s" % entry, 2)
                if isinstance( entry, types.FunctionType ) or isinstance( entry, types.MethodType ):
                    for line in entry():
                        self._blacklist.append( line )
                else:
                    self.read_blacklist( entry )
        return self._blacklist

    def __imageDirPattern( self, package, buildTarget ):
        """ return base directory name for package related image directory """
        directory = "image"

        if package.subinfo.options.useCompilerType == True:
            directory += '-' + compiler.getCompilerName()
        if package.subinfo.options.useBuildType == True:
            directory += '-' + package.buildType()
        directory += '-' + buildTarget
        return directory


    def __getImageDirectories( self ):
        """ return the image directories where the files are stored """
        imageDirs = []
        depList = []
        depList = portage.solveDependencies(self.category, self.package, depList, DependencyType.Runtime)

        for x in depList:
            if portage.PortageInstance.isVirtualPackage(x.category, x.package):
                CraftDebug.debug("Ignoring package b/c it is virtual: %s/%s" % (x.category, x.package))
                continue

            _package = portage.getPackageInstance( x.category, x.package )

            imageDirs.append(( os.path.join( self.rootdir, "build", x.category, x.package,
                    self.__imageDirPattern( _package, _package.buildTarget )), _package.subinfo.options.merge.destinationPath , _package.subinfo.options.package.disableStriping ) )
            # this loop collects the files from all image directories
            CraftDebug.debug("__getImageDirectories: category: %s, package: %s, version: %s, defaultTarget: %s" % (_package.category, x.package, _package.version, _package.buildTarget), 2)

        if craftSettings.getboolean("QtSDK", "Enabled", False) and craftSettings.getboolean("QtSDK", "PackageQtSDK", True):
            imageDirs.append((os.path.join( craftSettings.get("QtSDK", "Path") , craftSettings.get("QtSDK", "Version"), craftSettings.get("QtSDK", "Compiler")), None, False))

        return imageDirs

    def __toRegExp(self, fname, targetName) -> re:
        """ Read regular expressions from fname """
        fname = os.path.join(self.packageDir(), fname)
        if not os.path.isfile(fname):
            CraftDebug.die("%s not found at: %s" % (targetName.capitalize(), os.path.abspath(fname)))
        regex = "("
        for line in fileinput.input(fname):
            # Cleanup white spaces / line endings
            line = line.splitlines()
            line = line[0].rstrip()
            if line.startswith("#") or len(line) == 0:
                continue
            try:
                tmp = "^%s$" % line
                regex += "%s|" % tmp
                re.compile(tmp, re.IGNORECASE) #for debug
                CraftDebug.debug("%s added to %s as %s" % (line, targetName, tmp), 2)
            except re.error:
                CraftDebug.die("%s is not a valid regexp" % tmp)
        return re.compile("%s)" % regex[:-2], re.IGNORECASE)

    def read_whitelist( self, fname ):
        """ Read regular expressions from fname """
        self._whitelist.append(self.__toRegExp(fname,"whitelist"))

    def read_blacklist( self, fname ):
        """ Read regular expressions from fname """
        self._blacklist.append(self.__toRegExp(fname, "blacklist"))

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
        CraftDebug.debug("Copying %s -> %s" % (srcDir, destDir))
        uniquebasenames = []
        self.unique_names = []
        duplicates = []

        for entry in self.traverse( srcDir, self.whitelisted, self.blacklisted ):
            if os.path.basename( entry ) in uniquebasenames:
                CraftDebug.debug("Found duplicate filename: %s" % os.path.basename(entry), 2)
                duplicates.append( entry )
            else:
                self.unique_names.append( entry )
                uniquebasenames.append( os.path.basename( entry ) )

        for entry in self.unique_names:
            entry_target = entry.replace( srcDir, os.path.join( destDir + os.path.sep ) )
            if not os.path.exists( os.path.dirname( entry_target ) ):
                utils.createDir( os.path.dirname( entry_target ) )
            shutil.copy( entry, entry_target )
            CraftDebug.debug("Copied %s to %s" % (entry, entry_target), 2)
            if not strip and (entry_target.endswith(".dll") or entry_target.endswith(".exe")):
                self.strip( entry_target )
        for entry in duplicates:
            entry_target = entry.replace( srcDir, destDir + os.path.sep)
            if not os.path.exists( os.path.dirname( entry_target ) ):
                utils.createDir( os.path.dirname( entry_target ) )
            shutil.copy( entry, entry_target )
            CraftDebug.debug("Copied %s to %s" % (entry, entry_target), 2)
            if not strip and (entry_target.endswith(".dll") or entry_target.endswith(".exe")):
                self.strip( entry_target )
          
    def internalCreatePackage( self ):
        """ create a package """

        archiveDir = self.archiveDir()

        if not self.noClean:
            CraftDebug.debug("cleaning package dir: %s" % archiveDir)
            utils.cleanDirectory(archiveDir)
            for directory, mergeDir, strip  in self.__getImageDirectories():
                imageDir = archiveDir
                if mergeDir:
                    imageDir = os.path.join( imageDir, mergeDir )
                if os.path.exists( directory ):
                    self.copyFiles(directory, imageDir, strip)
                else:
                    CraftDebug.die("image directory %s does not exist!" % directory)

        if not os.path.exists( archiveDir ):
            os.makedirs( archiveDir )

        return True

        
    def preArchive(self):
        return True
