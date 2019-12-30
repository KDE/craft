# -*- coding: utf-8 -*-
# Copyright Hannah von Reth <vonreth@kde.org>
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
# copyright (c) 2009 Patrick Spendrin <ps_ml@gmx.de>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

# git support
import io

from Source.VersionSystemSourceBase import *


## \todo requires installed git package -> add suport for installing packages

class GitSource(VersionSystemSourceBase):
    """git support"""

    def __init__(self, subinfo=None):
        CraftCore.debug.trace('GitSource __init__')
        if subinfo:
            self.subinfo = subinfo
        VersionSystemSourceBase.__init__(self)

    def __getCurrentBranch(self):
        if os.path.exists(self.checkoutDir()):
            with io.StringIO() as tmp:
                self.__git("rev-parse", ["--abbrev-ref", "HEAD"], stdout=tmp)
                return tmp.getvalue().strip()
        return None

    def __isLocalBranch(self, branch):
        if os.path.exists(self.checkoutDir()):
            with io.StringIO() as tmp:
                self.__git("for-each-ref", ["--format=%(refname:short)", "refs/heads"], stdout=tmp)
                return branch in tmp.getvalue().strip().split("\n")
        return False

    def __isTag(self, _tag):
        if os.path.exists(self.checkoutDir()):
            with io.StringIO() as tmp:
                self.__git("tag", stdout=tmp)
                return _tag in tmp.getvalue().strip().split("\n")
        return False

    def __updateSubmodeule(self):
        if self.subinfo.options.fetch.checkoutSubmodules:
            return self.__git("submodule", ["update", "--init", "--recursive"])
        return True

    def __getCurrentRevision(self):
        """return the revision returned by git show"""

        # run the command
        branch = self.__getCurrentBranch()
        if not self.__isTag(branch):
            with io.StringIO() as tmp:
                self.__git("rev-parse", ["--short", "HEAD"], stdout=tmp)
                return f"{branch}-{tmp.getvalue().strip()}"
        else:
            # in case this is a tag, print out the tag version
            return branch

    def __git(self, command, args=None, logCommand=False, **kwargs):
        """executes a git command in a shell.
        Default for cwd is self.checkoutDir()"""
        parts = ["git", command]
        if command in ("clone", "checkout", "fetch", "pull", "submodule"):
            if CraftCore.debug.verbose() < 0:
                parts += ["-q"]
            else:
                kwargs["displayProgress"] = True
        else:
            kwargs["logCommand"] = logCommand
        if args:
            parts += args
        if not kwargs.get("cwd"):
            kwargs["cwd"] = self.checkoutDir()
        return utils.system(parts, **kwargs)

    def fetch(self):
        CraftCore.debug.trace('GitSource fetch')
        # get the path where the repositories should be stored to

        repopath = self.repositoryUrl()
        CraftCore.log.debug("fetching %s" % repopath)

        # in case you need to move from a read only Url to a writeable one, here it gets replaced
        repopath = repopath.replace("[git]", "")

        repoString = utils.replaceVCSUrl(repopath)
        [repoUrl, repoBranch, repoTag] = utils.splitVCSUrl(repoString)

        # override tag
        if self.subinfo.options.dynamic.revision:
            repoTag = self.subinfo.options.dynamic.revision
            repoBranch = ""

        # override the branch
        if self.subinfo.options.dynamic.branch:
            repoBranch = self.subinfo.options.dynamic.branch

        if repoTag and repoBranch:
            CraftCore.log.error(f"Your not allowed to specify a branch and a tag: branch -> {repoBranch},  tag -> {repoTag}")
            return False

        if not repoBranch and not repoTag:
            repoBranch = "master"

        # only run if wanted (e.g. no --offline is given on the commandline)
        if (self.noFetch):
            CraftCore.log.debug("skipping git fetch (--offline)")
            return True
        else:
            ret = True
            checkoutDir = self.checkoutDir()
            # if we only have the checkoutdir but no .git within,
            # clean this up first
            if os.path.exists(checkoutDir) \
                    and not os.path.exists(os.path.join(checkoutDir, ".git")):
                os.rmdir(checkoutDir)
            if os.path.isdir(checkoutDir):
                if not repoTag:
                    ret = (self.__git("fetch")
                          and self.__git("checkout", [repoBranch or "master"])
                          and self.__git("merge"))
            else:
                args = []
                # it doesn't exist so clone the repo
                os.makedirs(checkoutDir)
                # first try to replace with a repo url from etc/blueprints/crafthosts.conf
                if self.subinfo.options.fetch.checkoutSubmodules:
                    args += ["--recursive"]
                ret = self.__git('clone', args + [repoUrl, self.checkoutDir()])

            # if a branch is given, we should check first if the branch is already downloaded
            # locally, otherwise we can track the remote branch
            if ret and repoBranch and not repoTag:
                if not self.__isLocalBranch(repoBranch):
                    track = ["--track", f"origin/{repoBranch}"]
                else:
                    track = [repoBranch]
                ret = self.__git("checkout", track)

            # we can have tags or revisions in repoTag
            if ret and repoTag:
                if self.__isTag(repoTag):
                    if not self.__isLocalBranch("_" + repoTag):
                        ret = self.__git('checkout', ['-b', f"_{repoTag}", repoTag])
                    else:
                        ret = self.__git('checkout', [f"_{repoTag}"])
                else:
                    # unknown tag, try to fetch it first
                    self.__git('fetch', ['--tags'])

                    ret = self.__git('checkout', [repoTag])
        return ret and self.__updateSubmodeule()

    def applyPatch(self, fileName, patchdepth, unusedSrcDir=None):
        """apply single patch o git repository"""
        CraftCore.debug.trace('GitSource ')
        if fileName:
            patchfile = os.path.join(self.packageDir(), fileName)
            return self.__git('apply', ['--ignore-space-change',
                              '-p', str(patchdepth), patchfile], logCommand=True)
        return True

    def createPatch(self):
        """create patch file from git source into the related package dir.
        The patch file is named autocreated.patch"""
        CraftCore.debug.trace('GitSource createPatch')
        patchFileName = os.path.join(self.packageDir(), "%s-%s.patch" % \
                                     (self.package.name, str(datetime.date.today()).replace('-', '')))
        CraftCore.log.debug("git diff %s" % patchFileName)
        with open(patchFileName, 'wt+') as patchFile:
            return self.__git('diff', stdout=patchFile)

    def sourceVersion(self):
        """print the revision returned by git show"""
        CraftCore.debug.trace('GitSource sourceVersion')

        return self.__getCurrentRevision()

    def checkoutDir(self, index=0):
        CraftCore.debug.trace('GitSource checkoutDir')
        return VersionSystemSourceBase.checkoutDir(self, index)

    def sourceDir(self, index=0):
        CraftCore.debug.trace('GitSource sourceDir')
        repopath = self.repositoryUrl()
        # in case you need to move from a read only Url to a writeable one, here it gets replaced
        repopath = repopath.replace("[git]", "")
        sourcedir = self.checkoutDir(index)

        if self.subinfo.hasTargetSourcePath():
            sourcedir = os.path.join(sourcedir, self.subinfo.targetSourcePath())

        CraftCore.log.debug("using sourcedir: %s" % sourcedir)
        parent, child = os.path.split(sourcedir)
        return os.path.join(CraftShortPath(parent).shortPath, child)

    def getUrls(self):
        """print the url where to clone from and the branch/tag/hash"""
        # in case you need to move from a read only Url to a writeable one, here it gets replaced
        repopath = self.repositoryUrl().replace("[git]", "")
        repoString = utils.replaceVCSUrl(repopath)
        [repoUrl, repoBranch, repoTag] = utils.splitVCSUrl(repoString)
        if not repoBranch and not repoTag:
            repoBranch = "master"
        print('|'.join([repoUrl, repoBranch, repoTag]))
        return True
