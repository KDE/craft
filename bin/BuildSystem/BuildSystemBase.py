# 
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

""" \package BuildSystemBase"""

from EmergeBase import *
import utils;

EMERGE_MAKE_PROGRAM=os.getenv( "EMERGE_MAKE_PROGRAM" )

class BuildSystemBase(EmergeBase):
    """provides a generic interface for build systems and implements all stuff for all build systems"""
    noClean = False
    debug = True

    def __init__(self,type,configureOptions="", makeOptions=""):
        """constructor"""
        EmergeBase.__init__(self)
        self.buildSystemType = type
        self.configureOptions = configureOptions
        self.makeOptions = makeOptions
        self.envPath = ""
        if self.compiler() == "mingw":
            self.envPath = "mingw/bin"
        if self.compiler() == "mingw4":
            self.envPath = "mingw4/bin"

        if self.compiler() == "msvc2005" or self.compiler() == "msvc2008":
            self.makeProgramm = "nmake /NOLOGO"
        elif self.compiler() == "mingw" or self.compiler() == "mingw4":
            self.makeProgramm = "mingw32-make"
        else:
            utils.die( "unknown %s compiler" % self.compiler() )
        if EMERGE_MAKE_PROGRAM:
            self.cmakeMakeProgramm = EMERGE_MAKE_PROGRAM
            utils.debug( "set custom make program: %s" % EMERGE_MAKE_PROGRAM, 1 )
                
    def configure(self): 
        """configure the target"""
        abstract()

    def install(self): 
        """install the target into local install directory"""
        abstract()

    def uninstall(self): 
        """uninstall the target from the local install directory"""
        abstract()

    def runTests(self): 
        """run the test - if available - for the target"""
        abstract()

    def make(self): 
        """make the target by runnning the related make tool"""
        abstract()
            
    def compile(self):
        """convencience method - runs configure() and make()"""
        return self.configure() and self.make()
    
    def configureSourceDir(self):
        """returns source dir used for configure step"""
        if hasattr(self,'source'):
            sourcedir = self.source.sourceDir()
        else:
            sourcedir = self.sourceDir()
       
        if self.subinfo.hasConfigurePath():
            sourcedir = os.path.join(sourcedir,self.subinfo.configurePath())
        return sourcedir
        
