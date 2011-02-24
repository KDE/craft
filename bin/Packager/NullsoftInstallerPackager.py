#
# copyright (c) 2010 Patrick Spendrin <ps_ml@gmx.de>
# copyright (c) 2010 Andre Heinecke <aheinecke@intevation.de> (code taken from the kdepim-ce-package.py)
#
from Packager.PackagerBase import *
import shutil
import re
import types
import fileinput
from _winreg import * # pylint: disable=F0401

class NSIPackagerLists(object):
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


class NullsoftInstallerPackager( PackagerBase ):
    """
Packager for Nullsoft scriptable install system

This Packager generates a nsis installer (an executable which contains all files)
from the image directories of emerge. This way you can be sure to have a clean
installer.

In your package, you can add regexp whitelists and blacklists (see example files
for the fileformat). The files for both white- and blacklists, must be given already
in the constructor.

You can override the .nsi default script and you will get the following defines
given into the nsis generator via commandline if you do not override the attributes
of the same name in the dictionary self.defines:
setupname:      PACKAGENAME-setup-BUILDTARGET.exe
                PACKAGENAME is the name of the package, if the package ends with "-package",
                that part is removed
srcdir:         is set to the image directory, where all files from the image directories
                of all dependencies are gathered. You shouldn't normally have to set this.
company:        sets the company name used for the registry key of the installer. Default
                value is "KDE".
productname:    contains the capitalized PACKAGENAME and the buildTarget of the current package
executable:     executable is defined empty by default, but it is used to add a link into the
                start menu.
You can add your own defines into self.defines as well.

The output directory is determined by the environment variable EMERGE_PKGDSTDIR.
if EMERGE_NOCLEAN is given (e.g. because you call emerge --update --package Packagename), the
file collection process is skipped, and only the installer is generated.
"""
    def __init__( self, whitelists=None, blacklists=None):
        PackagerBase.__init__( self, "NullsoftInstallerPackager" )
        if whitelists is None:
            whitelists = [ NSIPackagerLists.defaultWhitelist ]
        if blacklists is None:
            blacklists = [ NSIPackagerLists.defaultBlacklist ]
        self.nsisInstallPath = None
        self.isInstalled = self.__isInstalled()
        if not self.isInstalled:
            utils.die( "could not find installed nsis package, "
                       "you may download and install it from "
                       "http://sourceforge.net/projects/nsis/" )
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
        """ check if nsis (Nullsoft scriptable install system) is installed somewhere """
        # pylint: disable=E0602
        # if pylint is done on linux, we don't have those toys
        try:
            key = OpenKey( HKEY_LOCAL_MACHINE, r'SOFTWARE\NSIS', 0, KEY_READ )
        except WindowsError:
            try:
                key = OpenKey( HKEY_LOCAL_MACHINE, r'SOFTWARE\Wow6432Node\NSIS', 0, KEY_READ )
            except WindowsError:
                return False
        [ self.nsisInstallPath, dummyType ] = QueryValueEx( key, "" )
        return True

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
            defaultTarget = portage.findPossibleTargets( category, package, version )
            _package = portage.getPackageInstance( category, package, defaultTarget )
            imageDirs.append( ( os.path.join( self.__buildRoot( category, package, version ),
                    self.__imageDirPattern( _package, defaultTarget ) ), _package.subinfo.options.merge.destinationPath ) )
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
            filename that the function whitelist returns as true
        """
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

    def copyFiles( self, srcDir, destDir ):
        """
            Copy the binaries for the Package from srcDir to the imageDir
            directory
        """
        utils.createDir( destDir )
        utils.debug( "Copying from %s ..." % ( srcDir ) )
        uniquebasenames = []
        unique_names = []
        duplicates = []

        for entry in self.traverse( srcDir, self.whitelisted, self.blacklisted ):
            if os.path.basename( entry ) in uniquebasenames:
                utils.debug( "Found duplicate filename: %s" % os.path.basename( entry ), 2 )
                duplicates.append( entry )
            else:
                unique_names.append( entry )
                uniquebasenames.append( os.path.basename( entry ) )

        for entry in unique_names:
            entry_target = entry.replace( srcDir, os.path.join( destDir + os.path.sep ) )
            if not os.path.exists( os.path.dirname( entry_target ) ):
                utils.createDir( os.path.dirname( entry_target ) )
            shutil.copy( entry, entry_target )
            utils.debug( "Copied %s to %s" % ( entry, entry_target ), 2 )
        for entry in duplicates:
            entry_target = entry.replace( srcDir, os.path.join( destDir + os.path.sep ) )
            if not os.path.exists( os.path.dirname( entry_target ) ):
                utils.createDir( os.path.dirname( entry_target ) )
            shutil.copy( entry, entry_target )
            utils.debug( "Copied %s to %s" % ( entry, entry_target ), 2 )

    def generateNSISInstaller( self ):
        """ runs makensis to generate the installer itself """
        if self.package.endswith( "-package" ):
            self.shortPackage = self.package[ : -8 ]
        if not "setupname" in self.defines or not self.defines[ "setupname" ]:
            self.defines[ "setupname" ] = "%s-setup-%s.exe" % ( self.shortPackage, self.buildTarget )
        if not "srcdir" in self.defines or not self.defines[ "srcdir" ]:
            self.defines[ "srcdir" ] = self.imageDir()
        if not "company" in self.defines or not self.defines[ "company" ]:
            self.defines[ "company" ] = "KDE"
        if not "productname" in self.defines or not self.defines[ "productname" ]:
            self.defines[ "productname" ] = "%s %s" % ( self.shortPackage.capitalize(), self.buildTarget )
        if not "executable" in self.defines or not self.defines[ "executable" ]:
            self.defines[ "executable" ] = ""
        if not self.scriptname:
            self.scriptname = os.path.join( os.path.dirname( __file__ ), "NullsoftInstaller.nsi" )

        # make absolute path for output file
        if not os.path.isabs( self.defines[ "setupname" ] ):
            dstpath = self.packageDestinationDir()
            self.defines[ "setupname" ] = os.path.join( dstpath, self.defines[ "setupname" ] )

        definestring = ""
        for key in self.defines:
            definestring += " /D" + key + "=\"" + self.defines[ key ] + "\""

        utils.new_line()
        utils.debug( "generating installer %s" % self.defines[ "setupname" ] )
        if self.isInstalled:
            utils.systemWithoutShell( "\"%s\" %s %s" % ( os.path.join(
                self.nsisInstallPath, 'makensis.exe' ), definestring,
                self.scriptname ), cwd = os.path.abspath( self.packageDir() ) )

    def createPackage( self ):
        """ create a package """
        print "packaging using the NullsoftInstallerPackager"
        if not utils.envAsBool("EMERGE_NOCLEAN"):
            utils.debug( "cleaning imagedir: %s" % self.imageDir() )
            utils.cleanDirectory( self.imageDir() )
            for directory, mergeDir in self.__getImageDirectories():
                imageDir = self.imageDir()
                if mergeDir:
                    imageDir = os.path.join( imageDir, mergeDir )
                if os.path.exists( directory ):
                    self.copyFiles(directory, imageDir)
                else:
                    utils.die( "image directory %s does not exist!" % directory )

        if not os.path.exists( self.imageDir() ):
            os.makedirs( self.imageDir() )

        self.generateNSISInstaller()
        return True
