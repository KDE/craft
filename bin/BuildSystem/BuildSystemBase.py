# -*- coding: utf-8 -*-

from EmergeBase import *
import utils;

class BuildSystemBase(EmergeBase):
    """provides a generic interface for build systems and implements all stuff for all build systems"""
    noClean = False
    debug = True

    def __init__(self):
        EmergeBase.__init__(self)

    
    def configureOptions( self ):
        """options for the configure line"""
        return ""

    # todo find a better name 
    def configureTool(self):
        """return string to override the complete configure command"""
        return ""
        
    #configure the target
    # todo not sure if buildType and options are used anywhere, if not remove them
    def configure(self, buildType=None, customOptions=""): abstract

    #install the target into local install directory"""
    def install(self): abstract()

    #uninstall the target from the local install directory"""
    def uninstall(self): abstract()

    #run the test - if available - for the target"""
    def runTests(self): abstract()

    #make the target by runnning the related make tool"""
    def make(self, buildType=None): abstract()
            
    def makeOptions( self ):
        """options for the make command line"""
        return ""

    # todo not sure if buildType and customDefines are used anywhere, if not remove them
    def compile(self, buildType=None, customOptions=""):
        """convencience method - runs configure() and make()"""
        if( not self.buildType() == None ) :
            if( not ( self.configure( self.buildType(), customOptions ) and self.make( self.buildType() ) ) ):
                return False
            else:
                if( not ( self.configure( "Debug", customOptions ) and self.make( "Debug" ) ) ):
                    return False
                if( not ( self.configure( "Release", customOptions ) and self.make( "Release" ) ) ):
                    return False
            return True

    def setDirectories(self):
        return