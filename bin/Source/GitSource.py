# 
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
# copyright (c) 2009 Patrick Spendrin <ps_ml@gmx.de>
#
# git support

from VersionSystemSourceBase import *
import os
import utils
from shells import *

## \todo requires installed git package -> add suport for installing packages 

class GitSource ( VersionSystemSourceBase ):
    """git support"""
    def __init__( self ):
        VersionSystemSourceBase.__init__( self )
        # get a shell since git doesn't run natively at the moment
        self.shell = MSysShell()
        
        # detect git installation
        gitInstallDir = os.path.join( self.rootdir, 'dev-utils', 'git' )
        if os.path.exists( gitInstallDir ):
            self.shell.msysdir = gitInstallDir
            utils.debug( 'using shell from %s' % gitInstallDir, 1 )

    def fetch( self, repopath=None ):
        # get the path where the repositories should be stored to
        if repopath == None:
            repopath = self.repositoryUrl()
        
        # in case you need to move from a read only Url to a writeable one, here it gets replaced
        repopath = repopath.replace("[git]", "")
        repoString = utils.replaceGitUrl( repopath )
        [repoUrl, repoBranch, repoTag ] = utils.splitGitUrl( repoString )

        if utils.verbose() <= 2:
            devNull = " > /dev/null"
        else:
            devNull = ""
        ret = True
        # only run if wanted (e.g. no --offline is given on the commandline)
        if ( not self.noFetch ):
            self.setProxy()
            safePath = os.environ["PATH"]
            # add the git path to the PATH variable so that git can be called without path
            os.environ["PATH"] = os.path.join( self.rootdir, "git", "bin" ) + ";" + safePath
            if os.path.exists( self.sourceDir() ):
                # if directory already exists, simply do a pull but obey to offline
                ret = self.shell.execute( self.sourceDir(), "git", "pull" )
                
            else:
                # it doesn't exist so clone the repo
                os.makedirs( self.sourceDir() )
                # first try to replace with a repo url from etc/portage/emergehosts.conf
                ret = self.shell.execute( self.sourceDir(), "git", "clone %s ." % ( repoUrl ) )
                
            # if a branch is given, we should check first if the branch is already downloaded locally, or if we can track the remote branch
            # the following code is for both ways the same
            track = ""
            if ret and repoBranch:
                # grep is available already from the git package
                if not self.shell.execute( self.sourceDir(), "git", "branch | grep -E \"%s$\"%s" % ( repoBranch, devNull ) ):
                    track = "--track origin/"
            if ret and repoBranch:
                ret = self.shell.execute( self.sourceDir(), "git", "checkout %s%s" % ( track, repoBranch ) )
                
            # pay attention that after checkout of a tag, the next git pull might not work because of merging problems
            if ret and repoTag:
                ret = self.shell.execute( self.sourceDir(), "git", "checkout -b %s %s" % ( repoTag, repoTag ) )
        else:
            utils.debug( "skipping git fetch (--offline)" )
        return ret
    
    def applyPatches(self):
        """apply patches to git repository"""
        utils.debug( "GitSource.applyPatches called", 2 )

        if self.subinfo.hasTarget() or self.subinfo.hasSvnTarget():
            ( file, patchdepth ) = self.subinfo.patchesToApply()
            if file:
                patchfile = os.path.join ( self.packageDir(), file )
                return self.shell.execute( self.sourceDir(), "git", "apply -p %s %s" % (patchdepth, self.shell.toNativePath(patchfile)) )
        return True

    def createPatch( self ):
        """create patch file from git source into the related package dir. The patch file is named autocreated.patch"""
        ret = self.shell.execute( self.sourceDir(), "git", "diff > %s" % self.shell.toNativePath( os.path.join( self.packageDir(), "%s-%s.patch" % ( self.package, str( datetime.date.today() ).replace('-', '') ) ) ) )
        return ret

    def sourceVersion( self ):
        """ return the revision returned by git show """
        # open a temporary file - do not use generic tmpfile because this doesn't give a good file object with python
        tempfile = open( os.path.join( self.sourceDir().replace('/', '\\'), ".emergegitshow.tmp" ), "wb+" )
        
        # run the command
        self.shell.execute( self.sourceDir(), "git", "show --abbrev-commit", out=tempfile )
        tempfile.seek( os.SEEK_SET )

        # read the temporary file and grab the first line
        revision = tempfile.readline().replace("commit ", "").strip()
        tempfile.close()
        
        # print the revision - everything else should be quiet now
        print revision
        os.remove( os.path.join( self.sourceDir().replace('/', '\\'), ".emergegitshow.tmp" ) )
        return True