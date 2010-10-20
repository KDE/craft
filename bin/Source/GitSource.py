# 
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
# copyright (c) 2009 Patrick Spendrin <ps_ml@gmx.de>
#
# git support

from VersionSystemSourceBase import *
import os
import utils
import re
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

    def __fetchSingleBranch(self, repopath=None):
        # get the path where the repositories should be stored to
        if repopath == None:
            repopath = self.repositoryUrl()
        
        # in case you need to move from a read only Url to a writeable one, here it gets replaced
        repopath = repopath.replace("[git]", "")
        repoString = utils.replaceVCSUrl( repopath )
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
            isCommit = re.search( '\\b[0-9a-fA-F]{40}\\b', repoTag )
            if os.path.exists( self.checkoutDir() ):
                # if directory already exists, simply do a pull
                if not isCommit :
                    # our tag is a specific sha1sum we dont need to pull
                    ret = self.shell.execute( self.checkoutDir(), "git", "pull" )
            else:
                # it doesn't exist so clone the repo
                os.makedirs( self.checkoutDir() )
                # first try to replace with a repo url from etc/portage/emergehosts.conf
                ret = self.shell.execute( self.checkoutDir(), "git", "clone %s ." % ( repoUrl ) )
                
            # if a branch is given, we should check first if the branch is already downloaded locally, or if we can track the remote branch
            # the following code is for both ways the same
            track = ""
            if ret and repoBranch:
                # grep is available already from the git package
                if not self.shell.execute( self.checkoutDir(), "git", "branch | grep -E \"%s$\"%s" % ( repoBranch, devNull ) ):
                    track = "--track origin/"
            if ret and repoBranch:
                ret = self.shell.execute( self.checkoutDir(), "git", "checkout %s%s" % ( track, repoBranch ) )
                
            # pay attention that after checkout of a tag, the next git pull might not work because of merging problems
            if ret and repoTag:
                if not isCommit:
                    ret = self.shell.execute( self.checkoutDir(), "git",
                            "checkout -b %s %s" % ( repoTag, repoTag ) )
                else:
                    ret = self.shell.execute( self.checkoutDir(), "git",
                            "checkout %s" % repoTag )
        else:
            utils.debug( "skipping git fetch (--offline)" )
        return ret
    
    def __fetchMultipleBranch(self, repopath=None):
        # get the path where the repositories should be stored to
        if repopath == None:
            repopath = self.repositoryUrl()
        
        # in case you need to move from a read only Url to a writeable one, here it gets replaced
        repopath = repopath.replace("[git]", "")
        repoString = utils.replaceVCSUrl( repopath )
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
            rootCheckoutDir = os.path.join(self.checkoutDir(),'.git')
            if not os.path.exists( rootCheckoutDir ):
                # it doesn't exist so clone the repo
                os.makedirs( rootCheckoutDir )
                ret = self.shell.execute( self.shell.toNativePath(rootCheckoutDir), "git", "clone --mirror %s ." % ( repoUrl ) )
                
            if repoBranch == "":
                repoBranch = "master"
            if ret:
                branchDir = os.path.join(self.checkoutDir(),repoBranch)
                if not os.path.exists(branchDir):
                    os.makedirs(branchDir)
                    ret = self.shell.execute(branchDir, "git", "clone --local --shared -b %s %s %s" % \
                        (repoBranch, self.shell.toNativePath(rootCheckoutDir), self.shell.toNativePath(branchDir)))
            if ret: 
                #ret = self.shell.execute(branchDir, "git", "checkout -f")
                if repoTag:
                    ret = self.shell.execute(branchDir, "git", "checkout -f %s" % (repoTag))
                else:
                    ret = self.shell.execute(branchDir, "git", "checkout -f %s" % (repoBranch))
        else:
            utils.debug( "skipping git fetch (--offline)" )
        return ret
        
    
    def fetch(self, repopath=None):
        if os.getenv("EMERGE_GIT_MULTIBRANCH") == "1":
            return self.__fetchMultipleBranch(repopath)
        else:
            return self.__fetchSingleBranch(repopath)

    def applyPatch(self, file, patchdepth):
        """apply single patch o git repository"""
        if file:
            patchfile = os.path.join ( self.packageDir(), file )
            if os.getenv("EMERGE_GIT_MULTIBRANCH") == "1":
                repopath = self.repositoryUrl()
                # in case you need to move from a read only Url to a writeable one, here it gets replaced
                repopath = repopath.replace("[git]", "")
                repoString = utils.replaceVCSUrl( repopath )
                [repoUrl, repoBranch, repoTag ] = utils.splitGitUrl( repoString )
                if repoBranch == "":
                    repoBranch = "master"
                sourceDir = os.path.join(self.checkoutDir(),repoBranch)
                return self.shell.execute(sourceDir, "git", "apply --whitespace=fix -p %s %s" % \
                        (patchdepth, self.shell.toNativePath(patchfile)))
            else:
                sourceDir = self.sourceDir()            
                #FIXME this reverts previously applied patches !
                #self.shell.execute(sourceDir, "git", "checkout -f")
                return self.shell.execute(sourceDir, "git", "apply --whitespace=fix -p %s %s" % \
                        (patchdepth, self.shell.toNativePath(patchfile)))
        return True

    def createPatch( self ):
        """create patch file from git source into the related package dir. The patch file is named autocreated.patch"""
        ret = self.shell.execute( self.sourceDir(), "git", "diff --ignore-all-space > %s" % \
                self.shell.toNativePath( os.path.join( self.packageDir(), "%s-%s.patch" % \
                ( self.package, str( datetime.date.today() ).replace('-', '') ) ) ) )
        return ret

    def sourceVersion( self ):
        """ return the revision returned by git show """
        # open a temporary file - do not use generic tmpfile because this doesn't give a good file object with python
        tempfile = open( os.path.join( self.checkoutDir().replace('/', '\\'), ".emergegitshow.tmp" ), "wb+" )
        
        # run the command
        self.shell.execute( self.checkoutDir(), "git", "show --abbrev-commit", out=tempfile )
        tempfile.seek( os.SEEK_SET )

        # read the temporary file and grab the first line
        revision = tempfile.readline().replace("commit ", "").strip()
        tempfile.close()
        
        # print the revision - everything else should be quiet now
        print revision
        os.remove( os.path.join( self.checkoutDir().replace('/', '\\'), ".emergegitshow.tmp" ) )
        return True
        
    def sourceDir(self, index=0 ): 
        repopath = self.repositoryUrl()
        # in case you need to move from a read only Url to a writeable one, here it gets replaced
        repopath = repopath.replace("[git]", "")
        repoString = utils.replaceVCSUrl( repopath )
        [repoUrl, repoBranch, repoTag ] = utils.splitGitUrl( repoString )
        if repoBranch == "":
            repoBranch = "master"
        if os.getenv("EMERGE_GIT_MULTIBRANCH") == "1":
            sourcedir = os.path.join(self.checkoutDir(index),repoBranch)
        else:
            sourcedir = self.checkoutDir(index)

        if self.subinfo.hasTargetSourcePath():
            sourcedir = os.path.join(sourcedir, self.subinfo.targetSourcePath())

        utils.debug("using sourcedir: %s" % sourcedir,2)
        return sourcedir

