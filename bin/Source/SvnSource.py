# -*- coding: utf-8 -*-
# subversion support
## \todo needs dev-utils/subversion package, add some kind of tool requirement tracking for SourceBase derived classes 

from VersionSystemSourceBase import *
import os
import utils

class SvnSource (VersionSystemSourceBase):
    """subversion support"""
    def __init__(self):
        VersionSystemSourceBase.__init__(self)
        ## \todo add internal dependency for subversion package
        self.svnInstallDir = os.path.join(self.rootdir,'dev-utils','svn','bin')
        if not os.path.exists(self.svnInstallDir):
            utils.die("required subversion package not installed")
        
    def fetch( self, repopath=None ):
        """ checkout or update an existing repository path """
        if self.noFetch:
            utils.debug( "skipping svn fetch (--offline)" )
            return True
        
        if repopath == None:
            repopath = self.repositoryPath()

        if self.subinfo.hasSvnTarget():
            url = self.subinfo.svnTarget()
            if url.find("://") == -1:
                """ this is a KDE checkout """
                
                svndir = os.getenv("KDESVNDIR")
                if ( not os.path.exists( svndir ) ):
                        os.mkdir( svndir )

                # get the base repourl, in case of KDE svn it is svn://anonsvn.kde.org/home/kde/
                repourl = self.repositoryBasePath()

                # loop over the subdirectories
                for tmpdir in url.split( "/" )[:-1]:
                    if ( tmpdir == "" ):
                            continue
                    if utils.verbose() > 1:
                        print "  svndir: %s" % svndir
                        print "  dir to checkout: %s" % tmpdir
                        print "  repourl", repourl

                    self.__kdesinglecheckout( repourl, svndir, tmpdir, False )
                    svndir = os.path.join( svndir, tmpdir )
                    repourl = repourl + tmpdir + "/"

                if utils.verbose() > 0:
                    print "dir in which to really checkout: %s" % svndir
                    print "dir to really checkout: %s" % url.split( "/" )[-1]
                self.__kdesinglecheckout( repourl, svndir, url.split( "/" )[-1], True )
            else:
                if os.path.exists( self.sourceDir() ):
                    cmd = "%s/svn update %s %s" % ( self.svnInstallDir, repopath, self.sourceDir() )
                else:
                    cmd = "%s/svn checkout %s %s" % (self.svnInstallDir, repopath, self.sourceDir() )
                utils.system( cmd ) or utils.die( "while perfoming svn command: %s" % cmd )
        return True

    def __kdesinglecheckout( self, repourl, basepath, codir, doRecursive = False ):
        """in basepath try to checkout codir from repourl """
        """if codir exists and doRecursive is false, simply return,"""
        """if codir does not exist, but ownpath/.svn exists,"""
        """   do a svn update codir"""
        """else do svn co repourl/codir"""
        """if doRecursive is false, add -N to the svn command """

        if ( os.path.exists( os.path.join( basepath, codir ) ) and not doRecursive ):
            if utils.verbose() > 0:
                print "ksco exists:", basepath, codir
            return

        if ( doRecursive ):
                recFlag = ""
        else:
                recFlag = "--depth=files"

        if ( os.path.exists( os.path.join( basepath, codir, ".svn" ) ) ):
            # svn up
            svncmd = "%s/svn update %s %s" % (self.svnInstallDir, recFlag, codir )
        else:
            #svn co
            svncmd = "%s/svn checkout %s %s" % (self.svnInstallDir, recFlag, repourl + codir )

        if utils.verbose() > 1:
            print "kdesinglecheckout:pwd ", basepath
            print "kdesinglecheckout:   ", svncmd
        
        os.chdir( basepath )
        utils.system( svncmd ) or utils.die( "while checking out. cmd: %s" % svncmd )
