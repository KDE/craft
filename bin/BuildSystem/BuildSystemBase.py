# -*- coding: utf-8 -*-

from EmergeBase import *
import utils;

class BuildSystemBase(EmergeBase):
    """provides a generic interface for build systems and implements all stuff for all build systems"""
    
    """ build type """
    buildType = "Release"

    """ ? """
    buildNameExt = ""

    """ ? """
    workdir = ""

    """ ? """
    COMPILER = ""

    noClean = False
    
    debug = True

    def __init__(self):
        EmergeBase.__init__(self)

    #configure the target
    def configure(self,buildType="",customDefines=""): abstract

    def compile(self,buildType="",customDefines=""):
        """convencience method - runs configure() and make()"""
        if( not self.buildType == None ) :
            if( not ( self.configure( self.buildType, customDefines ) and self.make( self.buildType ) ) ):
                return False
            else:
                if( not ( self.configure( "Debug", customDefines ) and self.make( "Debug" ) ) ):
                    return False
                if( not ( self.configure( "Release", customDefines ) and self.make( "Release" ) ) ):
                    return False
            return True

    #install the target into local install directory"""
    def install(self): abstract()

    #uninstall the target from the local install directory"""
    def uninstall(self): abstract()

    #run the test - if available - for the target"""
    def runTests(self): abstract()

    #make the target by runnning the related make tool"""
    def make(self): abstract()
            
    def setDirectories(self):
        print "setDirectories called"
        return True