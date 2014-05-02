# -*- coding: utf-8 -*-
# central instance for managing settings regarding emerge
# copyright:
# Patrick von Reth <vonreth [AT] kde [DOT] org>


import argparse
import configparser
import os
import re
import sys


emergeSettings = None

def nomalizePath(path):
    if path.endswith( ":" ):
        path += "\\"
    return path

def emergeRoot( allowShortpath = True ):
    if allowShortpath and not emergeSettings is None and emergeSettings.getboolean("ShortPath", "EMERGE_USE_SHORT_PATH", False):
        return  nomalizePath(emergeSettings.get( "ShortPath", "EMERGE_ROOT_DRIVE" ))
    return os.path.abspath( os.path.join( os.path.dirname( sys.argv[ 0 ] ), "..", ".." ) )


def etcDir( allowShortpath = True ):
    return os.path.join( emergeRoot( allowShortpath ), "etc" )


def etcPortageDir( allowShortpath = True ):
    """the etc directory for portage"""
    return os.path.join( etcDir( allowShortpath ), "portage" )


class EmergeConfig( object ):
    variablePatern = re.compile( "\$\{[A-Za-z0-9_]*\}", re.IGNORECASE )

    def __init__( self ):
        self._config = None
        self.iniPath = os.path.join( etcDir( False ), "kdesettings.ini" )
        self._alias = dict( )
        self._readSettings( )

        self.setDefault( "General", "DUMP_SETTINGS", "False" )
        self.addAlias( "EmergeDebug", "Verbose", "General", "EMERGE_VERBOSE" )
        self.addAlias( "EmergeDebug", "MeasureTime", "General", "EMERGE_MEASURE_TIME" )
        self.addAlias( "General", "UseHardlinks", "General", "EMERGE_USE_SYMLINKS" )


        self.args = self._parseArgs()


    def _parseArgs(self):
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
                             default = self.get( "General", "EMERGE_OPTIONS", "" ).split( ";" ),
                             help = "Set emerge property from string <OPTIONS>. An example for is \"cmake.openIDE=1\" see options.py for more informations." )
        parser.add_argument( "-z", "--outDateVCS", action = "store_true",
                             help = "if packages from version control system sources are installed, it marks them as out of date and rebuilds them (tags are not marked as out of date)." )
        parser.add_argument( "-sz", "--outDatePackage", action = "store_true",
                             help = "similar to -z, only that it acts only on the last package, and works as normal on the rest." )
        parser.add_argument( "-q", "--stayquiet", action = "store_true",
                             dest = "stayQuiet",
                             help = "quiet: there should be no output - The verbose level should be 0" )
        parser.add_argument( "-t", "--buildtests", action = "store_true", dest = "buildTests",
                             default = self.getboolean( "General", "EMERGE_BUILDTESTS", False ) )
        parser.add_argument( "-c", "--continue", action = "store_true", dest = "doContinue" )
        parser.add_argument( "--offline", action = "store_true",
                             default = self.getboolean( "General", "EMERGE_OFFLINE", False ),
                             help = "do not try to connect to the internet: KDE packages will try to use an existing source tree and other packages would try to use existing packages in the download directory.\
                              If that doesn't work, the build will fail." )
        parser.add_argument( "-f", "--force", action = "store_true", dest = "forced",
                             default = self.getboolean( "General", "EMERGE_FORCED", False ) )
        parser.add_argument( "--buildtype", choices = [ "Release", "RelWithDebInfo", "MinSizeRel" "Debug" ],
                             dest = "buildType",
                             default = self.get( "General", "EMERGE_BUILDTYPE", "RelWithDebInfo" ),
                             help = "This will override the build type set by the environment option EMERGE_BUILDTYPE ." )
        parser.add_argument( "-v", "--verbose", action = "count",
                             default = int(self.get("EmergeDebug", "Verbose","1")),
                             help = " verbose: increases the verbose level of emerge. Default is 1. verbose level 1 contains some notes from emerge, all output of cmake, make and other programs that are used.\
                              verbose level 2a dds an option VERBOSE=1 to make and emerge is more verbose highest level is verbose level 3." )
        parser.add_argument( "--trace", action = "store", default = int(self.get( "General", "EMERGE_TRACE", "0" )), type = int )
        parser.add_argument( "-i", "--ignoreInstalled", action = "store_true",
                             help = "ignore install: using this option will install a package over an existing install. This can be useful if you want to check some new code and your last build isn't that old." )
        parser.add_argument( "--target", action = "store",
                             help = "This will override the build of the default target. The default Target is marked with a star in the printout of --print-targets" )
        parser.add_argument( "--search", action = "store_true",
                             help = "This will search for a package or a description matching or similar to the search term." )
        parser.add_argument( "--nocopy", action = "store_true",
                             default = self.getboolean( "General", "EMERGE_NOCOPY", False ),
                             help = "this option is deprecated. In older releases emerge would have copied everything from the SVN source tree to a source directory under KDEROOT\\tmp - currently nocopy is applied\
                              by default if EMERGE_NOCOPY is not set to \"False\". Be aware that setting EMERGE_NOCOPY to \"False\" might slow down the build process, irritate you and increase the disk space roughly\
                               by the size of SVN source tree." )
        parser.add_argument( "--noclean", action = "store_true",
                             default = self.getboolean( "General", "EMERGE_NOCLEAN", False ),
                             help = "this option will try to use an existing build directory. Please handle this option with care - it will possibly break if the directory isn't existing." )
        parser.add_argument( "--clean", action = "store_false", dest = "noclean",
                             help = "oposite of --noclean" )
        parser.add_argument( "--patchlevel", action = "store",
                             default = self.get( "General", "EMERGE_PKGPATCHLVL", "" ),
                             help = "This will add a patch level when used together with --package" )
        parser.add_argument( "--log-dir", action = "store",
                             default = self.get( "General", "EMERGE_LOG_DIR", "" ),
                             help = "This will log the build output to a logfile in LOG_DIR for each package. Logging information is appended to existing logs." )
        parser.add_argument( "--dump-deps-file", action = "store", dest = "dumpDepsFile",
                             help = "Output the dependencies of this package as a csv file suitable for emerge server." )
        parser.add_argument( "--dt", action = "store", choices = [ "both", "runtime", "buildtime" ], default = "both",
                             dest = "dependencyType" )
        parser.add_argument("--print-installed", action = "store_true",
                            help = "This will show a list of all packages that are installed currently.")
        parser.add_argument("--print-installable", action = "store_true",
                            help = "his will give you a list of packages that can be installed. Currently you don't need to enter the category and package: only the package will be enough.")
        for x in sorted( [ "fetch", "unpack", "preconfigure", "configure", "compile", "make",
                                                 "install", "qmerge", "manifest", "package", "unmerge", "test",
                                                 "checkdigest", "dumpdeps",
                                                 "full-package", "cleanimage", "cleanbuild", "createpatch", "geturls",
                                                 "version-dir", "version-package",
                                                  "print-revision", "print-targets",
                                                 "install-deps", "update", "update-direct-deps" ]):
            parser.add_argument( "--%s" % x, action = "store_const" , dest = "action", const = x, default = "all" )
        parser.add_argument( "packageNames", nargs = argparse.REMAINDER )

        return parser.parse_args( )


    def _readSettings( self ):
        if not os.path.exists( self.iniPath ):
            print( "Could not find %s" % self.iniPath )
            exit( 1 )
        self._config = configparser.ConfigParser( )
        self._config.read( self.iniPath )
        clean = False
        #replace possible vatiables within a section
        while not clean:
            clean = True
            for section in self._config.keys( ):
                for key in self._config[ section ]:
                    val = self._config[ section ][ key ]
                    if self.variablePatern.match( val ):
                        clean = False
                        match = self.variablePatern.findall( val )[ 0 ]
                        self._config[ section ][ key ] = val.replace( match, self._config[ section ][ match[ 2:-1 ] ] )


    def __contains__( self, key ):
        return self._config and self._config.has_section( key[ 0 ] ) and key[ 1 ] in self._config[ key[ 0 ] ]


    def addAlias( self, group, key, destGroup, destKey ):
        self._alias[ (group, key) ] = (destGroup, destKey)

    def get( self, group, key, default = None ):
        if self.__contains__( (group, key) ):
            #print((group,key,self._config[ group ][ key ]))
            return self._config[ group ][ key ]
        if (group, key) in self._alias:
            dg, dk = self._alias[ (group, key) ]
            if (dg, dk) in self:
                print( "Warning: %s/%s is deprecated and has ben renamed to %s/%s" % (dg, dk, group, key ), file = sys.stderr )
                return self.get( dg, dk, default )
        if default != None:
            self.set( group, key, default )
            return default
        self._config[ group ][ key ]

    def getboolean(self,  group, key, default = False):
        val = self.get(group,key,str(default))
        return self._config._convert_to_boolean(val)


    def set( self, group, key, value ):
        if not self._config.has_section(group):
            self._config.add_section(group)
        self._config[ group ][ key ] = str(value)
        if self.get( "General", "DUMP_SETTINGS", "False" ) == "True":
            with open( self.iniPath + ".dump", 'wt+' ) as configfile:
                self._config.write( configfile )


    def setDefault( self, group, key, value ):
        if not ( group, key ) in self:
            self.set( group, key, value )


emergeSettings = EmergeConfig( )


