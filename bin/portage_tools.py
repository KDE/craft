#!/usr/bin/env python

import os
import tools
import subversion

class Portage( tools.Environment ):
    def __init__( self ):
        """ ctor """
        tools.Environment.__init__( self )
        self.PORTAGE_DIRS = []
        self.portage_repos = []
        if os.getenv( "EMERGE_PORTAGE_DIRS" ):
            for i in os.getenv( "EMERGE_PORTAGE_DIRS" ).split( os.pathsep ):
                self.PORTAGE_DIRS.append( i )
                # for the future: there needs to be some kind of settings class which collects the subversion settings for each repository
                # the setting via the environment variable has to be outdated then
                # this guesses you use your KDE account for the emerge checkout
                self.portage_repos.append( subversion.Repository() )
                
    def sync( self ):
        for repository in self.portage_repos:
            """"""
            if self.verbose() > 1:
                """"""
                print "svnpath:", repository.info.svnpath
            #repository.update()
        
    def list_packages( self ):
        """ return a list of all packages including the category, name, version and path of the script """
        instList = []
        for portage_dir in self.PORTAGE_DIRS:
            catdirs = os.listdir( portage_dir )

            for category in catdirs:
                if os.path.isdir( os.path.join( portage_dir, category ) ):
                    pakdirs = os.listdir( os.path.join( portage_dir, category ) )
                    if self.IGNORE_SUBVERSION in pakdirs:
                        pakdirs.remove( self.IGNORE_SUBVERSION )
                    for package in pakdirs:
                        if os.path.isdir( os.path.join( portage_dir, category, package ) ):
                            scriptdirs = os.listdir( os.path.join( portage_dir, category, package ) )
                            for script in scriptdirs:
                                if script.endswith( '.py' ):
                                    version = script.replace('.py', '').replace(package + '-', '')
                                    instList.append( [ category, package, version, os.path.join( portage_dir, category, package, script) ] )

        return instList

if __name__ == '__main__':
    Portage().runSelfTests()
