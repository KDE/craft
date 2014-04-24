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

    def __init__(self, typeName=""):
        """constructor"""
        EmergeBase.__init__(self)
        self.supportsNinja = False        
        self.supportsCCACHE = utils.envAsBool("EMERGE_USE_CCACHE") and compiler.isMinGW();
        self.buildSystemType = typeName
        self.envPath = ""
        if self.compiler() == "mingw":
            self.envPath = "mingw/bin"
        if self.compiler() == "mingw4":
            self.envPath = "mingw4/bin"


    def _getmakeProgram(self):
        if self.supportsNinja and utils.envAsBool("EMERGE_USE_NINJA"):
            return "ninja"
        EMERGE_MAKE_PROGRAM = os.getenv( "EMERGE_MAKE_PROGRAM" )
        if EMERGE_MAKE_PROGRAM and self.subinfo.options.make.supportsMultijob:
            utils.debug( "set custom make program: %s" % EMERGE_MAKE_PROGRAM, 1 )
            return EMERGE_MAKE_PROGRAM
        elif not self.subinfo.options.make.supportsMultijob:
            if "MAKE" in os.environ:
                del os.environ["MAKE"]
        if compiler.isMSVC() or compiler.isIntel() :
            return "nmake /NOLOGO"
        elif compiler.isMinGW():
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
        
        if self.supportsCCACHE:
            defines += " %s" % self.ccacheOptions()
        return defines

    def makeOptions(self, defines="", maybeVerbose=True):
        """return options for make command line"""
        if self.subinfo.options.make.ignoreErrors:
            defines += " -i"
        if self.subinfo.options.make.makeOptions:
            defines += " %s" % self.subinfo.options.make.makeOptions
        if maybeVerbose and utils.verbose() > 1:
            if self.supportsNinja and utils.envAsBool("EMERGE_USE_NINJA"):
                defines += " -v "
            else:
                defines += " VERBOSE=1 V=1"
        return defines

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

    def configure(self):
        return True
        
    def make(self):
        return True
        
    def install(self):

        # create post (un)install scripts
        for pkgtype in ['bin', 'lib', 'doc', 'src', 'dbg']:
            script = os.path.join( self.packageDir(), "post-install-%s.cmd" ) % pkgtype
            scriptName = "post-install-%s-%s.cmd" % ( self.package, pkgtype )
            # are there any cases there installDir should be honored ?
            destscript = os.path.join( self.imageDir(), "manifest", scriptName )
            if not os.path.exists( os.path.join( self.imageDir(), "manifest" ) ):
                utils.createDir( os.path.join( self.imageDir(), "manifest" ) )
            if os.path.exists( script ):
                utils.copyFile( script, destscript )
            script = os.path.join( self.packageDir(), "post-uninstall-%s.cmd" ) % pkgtype
            scriptName = "post-uninstall-%s-%s.cmd" % ( self.package, pkgtype )
            # are there any cases there installDir should be honored ?
            destscript = os.path.join( self.imageDir(), "manifest", scriptName )
            if not os.path.exists( os.path.join( self.imageDir(), "manifest" ) ):
                utils.createDir( os.path.join( self.imageDir(), "manifest" ) )
            if os.path.exists( script ):
                utils.copyFile( script, destscript )

        if self.subinfo.options.package.withDigests:
            if self.subinfo.options.package.packageFromSubDir:
                filesDir = os.path.join(self.imageDir(), self.subinfo.options.package.packageFromSubDir)
            else:
                filesDir = self.imageDir()
        return True

    def ccacheOptions(self):
        return ""