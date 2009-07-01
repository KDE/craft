# -*- coding: utf-8 -*-
# subversion support

from VersionSystemSourceBase import *
import os
import utils

class SvnSource (VersionSystemSourceBase):
    """subversion support"""
    def __init__(self):
        VersionSystemSourceBase.__init__(self)
        
    def __checkout( self, repourl, ownpath, codir, doRecursive = False ):
        """in ownpath try to checkout codir from repourl """
        """if codir exists and doRecursive is false, simply return,"""
        """if codir does not exist, but ownpath/.svn exists,"""
        """   do a svn update codir"""
        """else do svn co repourl/codir"""
        """if doRecursive is false, add -N to the svn command """

        if ( os.path.exists( os.path.join( ownpath, codir ) ) and not doRecursive ):
            if utils.verbose() > 0:
                print "ksco exists:", ownpath, codir
            return

        if ( doRecursive ):
                recFlag = ""
        else:
                recFlag = "--depth=files"

        if ( os.path.exists( os.path.join( ownpath, codir, ".svn" ) ) ):
            # svn up
            svncmd = "svn update %s %s" % ( recFlag, codir )
        else:
            #svn co
            svncmd = "svn checkout %s %s" % ( recFlag, repourl + codir )

        if utils.verbose() > 1:
            print "checkout:pwd ", ownpath
            print "checkout:   ", svncmd
        os.chdir( ownpath )
        utils.system( svncmd ) or utils.die( "while checking out. cmd: %s" % svncmd )

    def fetch( self, svnpath=None, packagedir=None ):
        """svnpath is the part of the repo url after /home/kde, for example"""
        """"trunk/kdesupport/", which leads to the package itself,"""
        """without the package"""

        if svnpath == None:
            svnpath = self.repositoryPath()

        if packagedir == None:
            packagedir = self.packagedir
            
        if utils.verbose() > 1:
            print "fetch called. svnpath: %s dir: %s" % ( svnpath, packagedir )

        if ( self.noFetch ):
            if utils.verbose() > 0:
                print "skipping svn fetch/update (--offline)"
            return True

        svndir = self.kdesvndir
        if ( not os.path.exists( svndir ) ):
                os.mkdir( svndir )

        repourl = self.kdesvnserver + "/home/kde/"

        for tmpdir in svnpath.split( "/" ):
            if ( tmpdir == "" ):
                    continue
            if utils.verbose() > 1:
                print "  svndir: %s" % svndir
                print "  dir to checkout: %s" % tmpdir
                print "  repourl", repourl

            self.__checkout( repourl, svndir, tmpdir, False )
            svndir = os.path.join( svndir, tmpdir )
            repourl = repourl + tmpdir + "/"

        if utils.verbose() > 0:
            print "dir in which to really checkout: %s" % svndir
            print "dir to really checkout: %s" % packagedir
        self.__checkout( repourl, svndir, packagedir, True )

        svndir = os.path.join( self.kdesvndir, svnpath ).replace( "/", "\\" )
        #repo = self.kdesvnserver + "/home/kde/" + svnpath + dir
        #utils.svnFetch( repo, svndir, self.kdesvnuser, self.kdesvnpass )
        if utils.verbose() > 1:
            print "kdesvndir", self.kdesvndir
            print "svndir", svndir
        self.svndir = os.path.join( svndir, packagedir )

        return True
