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
        VersionSystemSourceBase.__init__(self, "GitSource")

        # get a shell since git doesn't run natively at the moment
        self.shell = MSysShell()

        # detect git installation
        gitInstallDir = os.path.join( self.rootdir, 'dev-utils', 'git' )
        if os.path.exists( gitInstallDir ):
            self.shell.msysdir = gitInstallDir
            utils.debug( 'using shell from %s' % gitInstallDir, 1 )

    def __getCurrentBranch(self, coDir):
        if os.path.exists(coDir):
            tmpFile = tempfile.TemporaryFile()
            self.__git("branch", "-a", stdout=tmpFile, cwd=coDir)
            # TODO: check return value for success
            tmpFile.seek( 0 )
            for line in tmpFile:
                if line.startswith("*"):
                    return line[2:]

    def __isLocalBranch( self, branch ):
        coDir = self.checkoutDir()
        if os.path.exists(coDir):
            tmpFile = tempfile.TemporaryFile()
            self.__git("branch", stdout=tmpFile, cwd=coDir)
            # TODO: check return value for success
            tmpFile.seek( 0 )
            for line in tmpFile:
                if line[2:-1] == branch:
                    return True
        return False

    def __isTag( self, _tag ):
        coDir = self.checkoutDir()
        if os.path.exists(coDir):
            tmpFile = tempfile.TemporaryFile()
            self.__git("tag", stdout=tmpFile, cwd=coDir)
            # TODO: check return value for success
            tmpFile.seek( 0 )
            for line in tmpFile:
                if line[:-1] == _tag:
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
                    ret = self.__git("pull", "origin", repoBranch or "master")
                    if self.subinfo.options.fetch.checkoutSubmodules:
                        self.__git("submodule", "update --init --recursive")
            else:
                # it doesn't exist so clone the repo
                os.makedirs( checkoutDir )
                # first try to replace with a repo url from etc/portage/emergehosts.conf
                recursive = '--recursive ' if self.subinfo.options.fetch.checkoutSubmodules else ''
                ret = self.__git('clone', recursive, repoUrl, '.')

            # if a branch is given, we should check first if the branch is already downloaded
            # locally, otherwise we can track the remote branch
            if ret and repoBranch and not repoTag:
                track = ""
                if not self.__isLocalBranch( repoBranch ):
                    track = "--track origin/"
                ret = self.__git('checkout', "%s%s" % (track, repoBranch))

            # we can have tags or revisions in repoTag
            if ret and repoTag:
                if self.__isTag( repoTag ):
                    if not self.__isLocalBranch( "_" + repoTag ):
                        ret = self.__git('checkout', '-b', '_%s' % repoTag, repoTag)
                    else:
                        ret = self.__git('checkout', '_%s' % repoTag)
                else:
                    ret = self.__git('checkout', repoTag)

        else:
            utils.debug( "skipping git fetch (--offline)" )
        return ret

    def __git(self, command, *args, **kwargs):
        """executes a git command in a shell. Default for cwd is self.checkoutDir()
        make the interface similar to utils.system although we do not
        use it yet"""
        args = list(args) # what we get is a tuple
        args.insert(0, command)
        if command == 'clone' and os.getenv("EMERGE_LOG_DIR"):
            # if stdout/stderr is redirected, git clone hangs forever.
            # It does not with option -q (quiet)
            args.insert(1, '-q')
        cwd = kwargs.get('cwd', self.checkoutDir())
        return self.shell.execute(self.shell.toNativePath(cwd), 'git', ' '.join(args),
            out=kwargs.get('stdout'),
            err=kwargs.get('stderr'))

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
            rootCheckoutDir = os.path.join(self.checkoutDir(),'.git')
            if not os.path.exists( rootCheckoutDir ):
                # it doesn't exist so clone the repo
                os.makedirs( rootCheckoutDir )
                ret = self.__git('clone', '--mirror', repoUrl, '.', cwd=rootCheckoutDir)
            else:
                ret = self.__git('fetch', cwd=rootCheckoutDir)
                if not ret:
                    utils.die( "could not fetch remote data" )

            if repoBranch == "":
                repoBranch = "master"
            if ret:
                branchDir = os.path.join(self.checkoutDir(), repoBranch)
                if not os.path.exists(branchDir):
                    os.makedirs(branchDir)
                    ret = self.__git('clone', '--local --shared -b', repoBranch, rootCheckoutDir, branchDir, cwd=branchDir)
                else:
                    ret = self.__git('pull')
                    if not ret:
                        utils.die( "could not pull into branch %s" % repoBranch )

            if ret:
                #self.__git('checkout', '-f',cwd=branchDir)
                ret = self.__git("checkout", "-f", repoTag or repoBranch, cwd=branchDir)
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
                #FIXME this reverts previously applied patches !
                #self.__git('checkout', '-f')
                sourceDir = self.checkoutDir()
            return self.__git('apply', '--whitespace=fix',
                    '-p%d' % patchdepth, patchfile, cwd=sourceDir)
        return True

    def createPatch( self ):
        """create patch file from git source into the related package dir.
        The patch file is named autocreated.patch"""
        utils.trace( 'GitSource createPatch', 2 )
        patchFileName = os.path.join( self.packageDir(), "%s-%s.patch" % \
                ( self.package, str( datetime.date.today() ).replace('-', '') ))
        with open(patchFileName,'w') as patchFile:
            return self.__git('diff', '--ignore-all-space',
                    cwd=self.sourceDir(), stdout=patchFile)

    def sourceVersion( self ):
        """return the revision returned by git show"""
        utils.trace( 'GitSource sourceVersion', 2 )
        # open a temporary file - do not use generic tmpfile because this doesn't give a good file object with python

        # run the command
        coDir = self.checkoutDir()
        tagVersion = self.__getCurrentBranch(coDir)[ 1:]
        if not self.__isTag(tagVersion):
            with tempfile.TemporaryFile() as tmpFile:
                self.__git("show", "--abbrev-commit", stdout=tmpFile, cwd=coDir)
                tmpFile.seek( os.SEEK_SET )

                # read the temporary file and grab the first line
                revision = tmpFile.readline().replace("commit ", "").strip()

            # print the revision - everything else should be quiet now
            print revision
        else:
            # in case this is a tag, print out the tag version
            print tagVersion
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

