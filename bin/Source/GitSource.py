#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
# copyright (c) 2009 Patrick Spendrin <ps_ml@gmx.de>
#
# git support

from Source.VersionSystemSourceBase import *
from shells import *
import tempfile

## \todo requires installed git package -> add suport for installing packages

class GitSource ( VersionSystemSourceBase ):
    """git support"""
    def __init__(self, subinfo=None):
        utils.trace( 'GitSource __init__', 2 )
        if subinfo:
            self.subinfo = subinfo
        VersionSystemSourceBase.__init__( self )

        # get a shell since git doesn't run natively at the moment
        self.shell = MSysShell()

        # detect git installation
        gitInstallDir = os.path.join( self.rootdir, 'dev-utils', 'git' )
        if os.path.exists( gitInstallDir ):
            self.shell.msysdir = gitInstallDir
            utils.debug( 'using git from %s' % gitInstallDir, 1 )

    def __getCurrentBranch( self ):
        branch = None
        if os.path.exists( self.checkoutDir() ):
            tmpFile = tempfile.TemporaryFile()
            self.shell.execute( self.checkoutDir(), "git", "branch -a", out=tmpFile )
            # TODO: check return value for success
            tmpFile.seek( 0 )
            for line in tmpFile:
                if line.startswith("*"):
                    branch = line[2:].rstrip()
                    break
        return branch

    def __isLocalBranch( self, branch ):
        if os.path.exists( self.checkoutDir() ):
            tmpFile = tempfile.TemporaryFile()
            self.shell.execute( self.checkoutDir(), "git", "branch", out=tmpFile )
            # TODO: check return value for success
            tmpFile.seek( 0 )
            for line in tmpFile:
                if line[2:].rstrip() == branch:
                    return True
        return False

    def __isTag( self, _tag ):
        if os.path.exists( self.checkoutDir() ):
            tmpFile = tempfile.TemporaryFile()
            self.shell.execute( self.checkoutDir(), "git", "tag", out=tmpFile )
            # TODO: check return value for success
            tmpFile.seek( 0 )
            for line in tmpFile:
                if line.rstrip() == _tag:
                    return True
        return False

    def __fetchSingleBranch( self, repopath = None ):
        utils.trace( 'GitSource __fetchSingleBranch', 2 )
        # get the path where the repositories should be stored to
        if repopath == None:
            repopath = self.repositoryUrl()

        # in case you need to move from a read only Url to a writeable one, here it gets replaced
        repopath = repopath.replace( "[git]", "" )
        repoString = utils.replaceVCSUrl( repopath )
        [ repoUrl, repoBranch, repoTag ] = utils.splitGitUrl( repoString )
        if not repoBranch and not repoTag:
            repoBranch = "master"

        ret = True
        # only run if wanted (e.g. no --offline is given on the commandline)
        if ( not self.noFetch ):
            self.setProxy()
            safePath = os.environ[ "PATH" ]
            # add the git path to the PATH variable so that git can be called without path
            os.environ[ "PATH" ] = os.path.join( self.rootdir, "git", "bin" ) + ";" + safePath
            checkoutDir = self.checkoutDir()
            # if we only have the checkoutdir but no .git within,
            # clean this up first
            if os.path.exists(checkoutDir) \
                    and not os.path.exists(checkoutDir + "\.git"):
                os.rmdir(checkoutDir)
            if os.path.exists(checkoutDir):
                if not repoTag:
                    ret = self.shell.execute(checkoutDir, "git",
                            "pull origin %s" % repoBranch or "master" )
                    if self.subinfo.options.fetch.checkoutSubmodules:
                        self.shell.execute(checkoutDir, "git",
                            "submodule update --init --recursive")
            else:
                # it doesn't exist so clone the repo
                os.makedirs( checkoutDir )
                # first try to replace with a repo url from etc/portage/emergehosts.conf
                recursive = '--recursive' if self.subinfo.options.fetch.checkoutSubmodules else ''
                ret = self.shell.execute( checkoutDir, "git", "clone %s %s ." % (recursive, repoUrl ) )

            # if a branch is given, we should check first if the branch is already downloaded
            # locally, otherwise we can track the remote branch
            if ret and repoBranch and not repoTag:
                track = ""
                if not self.__isLocalBranch( repoBranch ):
                    track = "--track origin/"
                ret = self.shell.execute( checkoutDir, "git", "checkout %s%s" % ( track, repoBranch ) )

            # we can have tags or revisions in repoTag
            if ret and repoTag:
                if self.__isTag( repoTag ):
                    if not self.__isLocalBranch( "_" + repoTag ):
                        ret = self.shell.execute( checkoutDir, "git", "checkout -b _%s %s" % ( repoTag, repoTag ) )
                    else:
                        ret = self.shell.execute( checkoutDir, "git", "checkout _%s" % repoTag )
                else:
                    ret = self.shell.execute( checkoutDir, "git", "checkout %s" % repoTag )

        else:
            utils.debug( "skipping git fetch (--offline)" )
        return ret

    def __fetchMultipleBranch(self, repopath=None):
        utils.trace( 'GitSource __fetchMultipleBranch', 2 )
        # get the path where the repositories should be stored to
        if repopath == None:
            repopath = self.repositoryUrl()

        # in case you need to move from a read only Url to a writeable one, here it gets replaced
        repopath = repopath.replace("[git]", "")
        repoString = utils.replaceVCSUrl( repopath )
        [repoUrl, repoBranch, repoTag ] = utils.splitGitUrl( repoString )

        ret = True
        # only run if wanted (e.g. no --offline is given on the commandline)
        if ( not self.noFetch ):
            self.setProxy()
            safePath = os.environ["PATH"]
            # add the git path to the PATH variable so that git can be called without path
            os.environ["PATH"] = os.path.join( self.rootdir, "git", "bin" ) + ";" + safePath
            rootCheckoutDir = os.path.join(self.checkoutDir(), '.git')
            if not os.path.exists( rootCheckoutDir ):
                # it doesn't exist so clone the repo
                os.makedirs( rootCheckoutDir )
                ret = self.shell.execute( self.shell.toNativePath(rootCheckoutDir), "git", "clone --mirror %s ." % ( repoUrl ) )
            else:
                ret = self.shell.execute( self.shell.toNativePath(rootCheckoutDir), "git", "fetch")
                if not ret:
                    utils.die( "could not fetch remote data" )

            if repoBranch == "":
                repoBranch = "master"
            if ret:
                branchDir = os.path.join(self.checkoutDir(), repoBranch)
                if not os.path.exists(branchDir):
                    os.makedirs(branchDir)
                    ret = self.shell.execute(branchDir, "git", "clone --local --shared -b %s %s %s" % \
                        (repoBranch, self.shell.toNativePath(rootCheckoutDir), self.shell.toNativePath(branchDir)))
                else:
                    ret = self.shell.execute(branchDir, "git", "pull")
                    if not ret:
                        utils.die( "could not pull into branch %s" % repoBranch )

            if ret:
                #ret = self.shell.execute(branchDir, "git", "checkout -f")
                ret = self.shell.execute(branchDir, "git", "checkout -f %s" % (repoTag or repoBranch))
        else:
            utils.debug( "skipping git fetch (--offline)" )
        return ret


    def fetch(self, repopath=None):
        utils.trace( 'GitSource fetch', 2 )
        if utils.envAsBool("EMERGE_GIT_MULTIBRANCH"):
            return self.__fetchMultipleBranch(repopath)
        else:
            return self.__fetchSingleBranch(repopath)

    def applyPatch(self, fileName, patchdepth, unusedSrcDir=None):
        """apply single patch o git repository"""
        utils.trace( 'GitSource ', 2 )
        if fileName:
            patchfile = os.path.join ( self.packageDir(), fileName )
            if utils.envAsBool("EMERGE_GIT_MULTIBRANCH"):
                repopath = self.repositoryUrl()
                # in case you need to move from a read only Url to a writeable one, here it gets replaced
                repopath = repopath.replace("[git]", "")
                repoString = utils.replaceVCSUrl( repopath )
                repoBranch = utils.splitGitUrl( repoString )[1] or "master"
                sourceDir = os.path.join(self.checkoutDir(), repoBranch)
            else:
                sourceDir = self.sourceDir()
                #FIXME this reverts previously applied patches !
                #self.shell.execute(sourceDir, "git", "checkout -f")
            return self.shell.execute(sourceDir, "git", "apply --whitespace=fix -p %s %s" % \
                    (patchdepth, self.shell.toNativePath(patchfile)))
        return True

    def createPatch( self ):
        """create patch file from git source into the related package dir.
        The patch file is named autocreated.patch"""
        utils.trace( 'GitSource createPatch', 2 )
        patchFileName = os.path.join( self.packageDir(), "%s-%s.patch" % \
                ( self.package, str( datetime.date.today() ).replace('-', '') ) )
        return self.shell.execute( self.sourceDir(), "git", "diff > %s" % \
                self.shell.toNativePath( patchFileName) )

    def sourceVersion( self ):
        """print the revision returned by git show"""
        utils.trace( 'GitSource sourceVersion', 2 )

        # run the command
        if not self.__isTag( self.__getCurrentBranch()[ 1: ] ):
            # open a temporary file - do not use generic tmpfile because this doesn't give a good file object with python
            with tempfile.TemporaryFile() as tmpFile:
                self.shell.execute( self.checkoutDir(), "git", "show --abbrev-commit", out=tmpFile )
                tmpFile.seek( os.SEEK_SET )
                # read the temporary file and grab the first line
                # print the revision - everything else should be quiet now
                print tmpFile.readline().replace("commit ", "").strip()
        else:
            # in case this is a tag, print out the tag version
            print self.__getCurrentBranch()[ 1: ]
        return True

    def checkoutDir(self, index=0 ):
        utils.trace( 'GitSource checkoutDir', 2 )
        return VersionSystemSourceBase.checkoutDir( self, index )

    def sourceDir(self, index=0 ):
        utils.trace( 'GitSource sourceDir', 2 )
        repopath = self.repositoryUrl()
        # in case you need to move from a read only Url to a writeable one, here it gets replaced
        repopath = repopath.replace("[git]", "")
        repoString = utils.replaceVCSUrl( repopath )
        _, repoBranch, _ = utils.splitGitUrl( repoString )
        if repoBranch == "":
            repoBranch = "master"
        if utils.envAsBool("EMERGE_GIT_MULTIBRANCH"):
            sourcedir = os.path.join(self.checkoutDir(index), repoBranch)
        else:
            sourcedir = self.checkoutDir(index)

        if self.subinfo.hasTargetSourcePath():
            sourcedir = os.path.join(sourcedir, self.subinfo.targetSourcePath())

        utils.debug("using sourcedir: %s" % sourcedir, 2)
        return sourcedir

