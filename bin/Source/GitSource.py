#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
# copyright (c) 2009 Patrick Spendrin <ps_ml@gmx.de>
#
# git support

import tempfile

from CraftDebug import craftDebug
from Source.VersionSystemSourceBase import *


## \todo requires installed git package -> add suport for installing packages

class GitSource ( VersionSystemSourceBase ):
    """git support"""
    def __init__(self, subinfo=None):
        craftDebug.trace('GitSource __init__')
        if subinfo:
            self.subinfo = subinfo
        VersionSystemSourceBase.__init__( self )

    def __getCurrentBranch( self ):
        branch = None
        if os.path.exists( self.checkoutDir() ):
            tmpFile = tempfile.TemporaryFile()
            self.__git("branch -a", stdout=tmpFile )
            # TODO: check return value for success
            tmpFile.seek( 0 )
            for line in tmpFile:
                line = str(line,"UTF-8")
                if line.startswith("*"):
                    branch = line[2:].rstrip()
                    break
        return branch

    def __isLocalBranch( self, branch ):
        if os.path.exists( self.checkoutDir() ):
            tmpFile = tempfile.TemporaryFile()
            self.__git("branch", stdout=tmpFile )
            # TODO: check return value for success
            tmpFile.seek( 0 )
            for line in tmpFile:
                if str(line[2:].rstrip(), "UTF-8") == branch.rstrip():
                    return True
        return False

    def __isTag( self, _tag ):
        if os.path.exists( self.checkoutDir() ):
            tmpFile = tempfile.TemporaryFile()
            self.__git("tag", stdout=tmpFile )
            # TODO: check return value for success
            tmpFile.seek( 0 )
            for line in tmpFile:
                if str(line.rstrip(), "UTF-8") == _tag:
                    return True
        return False

    def __getCurrentRevision( self ):
        """return the revision returned by git show"""

        # run the command
        branch = self.__getCurrentBranch()
        if not self.__isTag( branch ):
            # open a temporary file - do not use generic tmpfile because this doesn't give a good file object with python
            with tempfile.TemporaryFile() as tmpFile:
                self.__git("show", "--abbrev-commit", stdout=tmpFile )
                tmpFile.seek( os.SEEK_SET )
                # read the temporary file and grab the first line
                # print the revision - everything else should be quiet now
                line = tmpFile.readline()
                return "%s-%s" % (branch, str(line, "UTF-8").replace("commit ", "").strip())
        else:
            # in case this is a tag, print out the tag version
            return branch

    def __git(self, command, *args, **kwargs):
        """executes a git command in a shell.
        Default for cwd is self.checkoutDir()"""
        displayProgress = False
        if command in ('clone', 'checkout', 'fetch', 'pull', 'submodule'):
            if craftDebug.verbose() < 0:
                command += ' -q'
            else:
                kwargs["displayProgress"]  = True
                command += ' --progress'
        parts = ["git", command]
        parts.extend(args)
        if not kwargs.get('cwd'):
            kwargs['cwd'] = self.checkoutDir()
        return self.system(' '.join(parts), **kwargs)

    def fetch(self):
        craftDebug.trace('GitSource fetch')
        # get the path where the repositories should be stored to

        repopath = self.repositoryUrl()
        craftDebug.log.debug("fetching %s" % repopath)

        # in case you need to move from a read only Url to a writeable one, here it gets replaced
        repopath = repopath.replace("[git]", "")

        repoString = utils.replaceVCSUrl(repopath)
        [repoUrl, repoBranch, repoTag] = utils.splitVCSUrl(repoString)
        if not repoBranch and not repoTag:
            repoBranch = "master"

        # only run if wanted (e.g. no --offline is given on the commandline)
        if (self.noFetch):
            craftDebug.log.debug("skipping git fetch (--offline)")
            return True
        else:
            ret = True
            self.setProxy()
            checkoutDir = self.checkoutDir()
            # if we only have the checkoutdir but no .git within,
            # clean this up first
            if os.path.exists(checkoutDir) \
                    and not os.path.exists(os.path.join(checkoutDir, ".git")):
                os.rmdir(checkoutDir)
            if os.path.exists(checkoutDir):
                if not repoTag:
                    ret = self.__git("fetch")\
                            and self.__git("checkout", repoBranch or "master") \
                            and self.__git("merge")
                    if self.subinfo.options.fetch.checkoutSubmodules:
                        ret = ret and self.__git("submodule update --init --recursive")
            else:
                # it doesn't exist so clone the repo
                os.makedirs(checkoutDir)
                # first try to replace with a repo url from etc/portage/crafthosts.conf
                recursive = '--recursive' if self.subinfo.options.fetch.checkoutSubmodules else ''
                ret = self.__git('clone', recursive, "--depth=1", repoUrl, '.')

            # if a branch is given, we should check first if the branch is already downloaded
            # locally, otherwise we can track the remote branch
            if ret and repoBranch and not repoTag:
                track = ""
                if not self.__isLocalBranch(repoBranch):
                    track = "--track origin/"
                ret = self.__git('checkout', "%s%s" % (track, repoBranch))

            # we can have tags or revisions in repoTag
            if ret and repoTag:
                if self.__isTag(repoTag):
                    if not self.__isLocalBranch("_" + repoTag):
                        ret = self.__git('checkout', '-b', '_%s' % repoTag, repoTag)
                    else:
                        ret = self.__git('checkout', '_%s' % repoTag)
                else:
                    ret = self.__git('checkout', repoTag)
        return ret


    def applyPatch(self, fileName, patchdepth, unusedSrcDir=None):
        """apply single patch o git repository"""
        craftDebug.trace('GitSource ')
        if fileName:
            patchfile = os.path.join ( self.packageDir(), fileName )
            sourceDir = self.sourceDir()
            #FIXME this reverts previously applied patches !
            #self.__git('checkout', '-f',cwd=sourceDir)
            sourceDir = self.checkoutDir()
            return self.__git('apply', '--whitespace=fix',
                    '-p %d' % patchdepth, patchfile, cwd=sourceDir)
        return True

    def createPatch( self ):
        """create patch file from git source into the related package dir.
        The patch file is named autocreated.patch"""
        craftDebug.trace('GitSource createPatch')
        patchFileName = os.path.join( self.packageDir(), "%s-%s.patch" % \
                ( self.package, str( datetime.date.today() ).replace('-', '') ) )
        craftDebug.log.debug("git diff %s" % patchFileName)
        with open(patchFileName,'wt+') as patchFile:
            return self.__git('diff', stdout=patchFile)

    def sourceVersion( self ):
        """print the revision returned by git show"""
        craftDebug.trace('GitSource sourceVersion')

        return self.__getCurrentRevision()

    def checkoutDir(self, index=0 ):
        craftDebug.trace('GitSource checkoutDir')
        return VersionSystemSourceBase.checkoutDir( self, index )

    def sourceDir(self, index=0 ):
        craftDebug.trace('GitSource sourceDir')
        repopath = self.repositoryUrl()
        # in case you need to move from a read only Url to a writeable one, here it gets replaced
        repopath = repopath.replace("[git]", "")
        sourcedir = self.checkoutDir(index)

        if self.subinfo.hasTargetSourcePath():
            sourcedir = os.path.join(sourcedir, self.subinfo.targetSourcePath())

        craftDebug.log.debug("using sourcedir: %s" % sourcedir)
        return sourcedir

    def getUrls( self ):
        """print the url where to clone from and the branch/tag/hash"""
        # in case you need to move from a read only Url to a writeable one, here it gets replaced
        repopath = self.repositoryUrl().replace( "[git]", "" )
        repoString = utils.replaceVCSUrl( repopath )
        [ repoUrl, repoBranch, repoTag ] = utils.splitVCSUrl( repoString )
        if not repoBranch and not repoTag:
            repoBranch = "master"
        print('|'.join([repoUrl, repoBranch, repoTag]))
        return True
