# 
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
# copyright (c) 2009 Patrick Spendrin <ps_ml@gmx.de>
#
# git support

from VersionSystemSourceBase import *;
import os;
import utils;
from shells import *;
import tempfile;

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
            if os.path.exists( self.checkoutDir() ):
                tmpFile = tempfile.TemporaryFile()
                self.shell.execute( self.checkoutDir(), "git", "status | grep -E \"On branch\"", out=tmpFile )
                tmpFile.seek( 0 )
                currentBranch = tmpFile.read().replace( "\n", "" ).replace( "# On branch ", "" )
                # if directory already exists, simply do a pull but obey to offline
                tmpFile2 = tempfile.TemporaryFile()
                self.shell.execute( self.checkoutDir(), "git", "status | grep -E \"nothing to commit\"", out=tmpFile2 )
                tmpFile2.seek( 0 )
                data = tmpFile2.read().replace( "\n", "" )
                changed = ( data == "" )
                if changed:
                    ret = self.shell.execute( self.checkoutDir(), "git", "stash" )
                ret = self.shell.execute( self.checkoutDir(), "git", "pull origin master" )
                print "changed:", changed, currentBranch != repoBranch, currentBranch != "_" + repoTag
                if changed and ( currentBranch == repoBranch or currentBranch == "_" + repoTag ):
                    ret = self.shell.execute( self.checkoutDir(), "git", "stash pop" )
                else:
                    if currentBranch != repoBranch and currentBranch != "_" + repoTag:
                        utils.warning( "change of branches! Please check conflict branch by hand!" )
                        if currentBranch != "_" + repoTag:
                            branch = "_" + repoTag
                        else:
                            branch = repoBranch
                        ret = self.shell.execute( self.checkoutDir(), "git", "stash branch %s" % ( currentBranch + "_vs_" + branch + "_conflict" ) )
                        self.shell.execute( self.checkoutDir(), "git", "commit -am \"Emergency commit %s\"" % ( currentBranch + "_vs_" + branch + "_conflict" ) )
            else:
                currentBranch = ""
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
                
            if ret and repoTag:
                if not self.shell.execute( self.checkoutDir(), "git", "tag | grep -E \"%s$\"%s" % ( repoTag, devNull ) ):
                    utils.warning( "no tag %s found, assuming revision hash" % repoTag )
                else:
                    utils.debug( "found tag %s" % repoTag, 1 )
                repoTagBranch = "_" + repoTag

                tmpFile3 = tempfile.TemporaryFile()
                self.shell.execute( self.checkoutDir(), "git", "branch | grep -E \"%s$\"" % repoTagBranch, out=tmpFile3 )
                tmpFile3.seek(0)
                data = tmpFile3.read().replace("\n", "")
                print data, data == ""
                if data == "":
                    track = "%s -b %s" % ( repoTag, repoTagBranch )
                else:
                    track = "%s" % repoTagBranch
                ret = self.shell.execute( self.checkoutDir(), "git", "checkout %s" % ( track ) )
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

