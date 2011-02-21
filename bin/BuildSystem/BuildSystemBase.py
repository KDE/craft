#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

""" \package BuildSystemBase"""

from EmergeBase import *
import compiler
from graphviz import *
import dependencies


class BuildSystemBase(EmergeBase):
    """provides a generic interface for build systems and implements all stuff for all build systems"""
    noClean = False
    debug = True

    def __init__(self, typeName, className=None):
        """constructor"""
        EmergeBase.__init__(self, className)
        self.buildSystemType = typeName
        self.envPath = ""
        if self.compiler() == "mingw":
            self.envPath = "mingw/bin"
        if self.compiler() == "mingw4":
            self.envPath = "mingw4/bin"


    def _getmakeProgram(self):
        EMERGE_MAKE_PROGRAM = os.getenv( "EMERGE_MAKE_PROGRAM" )
        if EMERGE_MAKE_PROGRAM and self.subinfo.options.make.supportsMultijob:
            utils.debug( "set custom make program: %s" % EMERGE_MAKE_PROGRAM, 1 )
            return EMERGE_MAKE_PROGRAM
        elif not self.subinfo.options.make.supportsMultijob:
            os.unsetenv("MAKE")
        if compiler.isMSVC():
            return "nmake /NOLOGO"
        elif compiler.isMinGW_WXX():
            return "gmake"
        elif compiler.isMinGW32():
            return "mingw32-make"
        else:
            utils.die( "unknown %s compiler" % self.compiler() )
    makeProgramm = property(_getmakeProgram)

    def compile(self):
        """convencience method - runs configure() and make()"""
        configure = getattr(self, 'configure')
        make = getattr(self, 'make')
        return configure() and make()

    def configureSourceDir(self):
        """returns source dir used for configure step"""
        # pylint: disable=E1101
        # this class never defines self.source, that happens only
        # in MultiSource.
        if hasattr(self,'source'):
            sourcedir = self.source.sourceDir()
        else:
            sourcedir = self.sourceDir()

        if self.subinfo.hasConfigurePath():
            sourcedir = os.path.join(sourcedir, self.subinfo.configurePath())
        return sourcedir

    def configureOptions(self, defines=""):
        """return options for configure command line"""
        if self.subinfo.options.configure.defines != None:
            defines += " %s" % self.subinfo.options.configure.defines
        return defines

    def makeOptions(self, defines="", maybeVerbose=True):
        """return options for make command line"""
        if self.subinfo.options.make.ignoreErrors:
            defines += " -i"
        if self.subinfo.options.make.makeOptions:
            defines += " %s" % self.subinfo.options.make.makeOptions
        if maybeVerbose and utils.verbose() > 1:
            defines += " VERBOSE=1"
        return defines

    def setupTargetToolchain(self):
        os.environ["PATH"] = os.environ["TARGET_PATH"]
        os.environ["INCLUDE"] = os.environ["TARGET_INCLUDE"]
        os.environ["LIB"] = os.environ["TARGET_LIB"]

    def dumpEmergeDependencies( self ):
        """dump emerge package dependencies"""
        output = dependencies.dumpDependencies( self.package )
        outDir = self.buildDir()
        outFile = os.path.join( outDir, self.package + '-emerge.dot' )
        if not os.path.exists( os.path.dirname( outFile ) ):
            os.makedirs( os.path.dirname( outFile ) )
        with open( outFile, "w" ) as f:
            f.write( output )

        graphviz = GraphViz( self )

        if not graphviz.runDot( outFile, outFile + '.pdf', 'pdf' ):
            return False

        return graphviz.openOutput()

    def dumpDependencies(self):
        """dump package dependencies """
        return self.dumpEmergeDependencies()
