# -*- coding: utf-8 -*-
""" \package BuildSystemBase"""

from EmergeBase import *
import utils;

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
                
    ## \todo not sure if buildType and options are used anywhere, if not remove them
    def configure(self, buildType=None): 
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

    def make(self, buildType=None): 
        """make the target by runnning the related make tool"""
        abstract()
            
    # \todo not sure if buildType and customDefines are used anywhere, if not remove them"""
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
    