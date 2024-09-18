#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
# subversion support
## \todo needs dev-utils/subversion package, add some kind of tool requirement tracking for SourceBase derived classes
import datetime
import os
import tempfile

import utils
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore
from CraftStandardDirs import CraftStandardDirs
from Source.VersionSystemSourceBase import VersionSystemSourceBase


class SvnSource(VersionSystemSourceBase):
    """subversion support"""

    def __init__(self, package: CraftPackageObject):
        CraftCore.debug.trace("SvnSource.__init__")
        super().__init__(package=package)

    def checkoutDir(self, index=0):
        CraftCore.debug.trace("SvnSource.checkoutDir")
        if self.subinfo.hasSvnTarget():
            u = self.getUrl(index)
            (url, _) = self.splitUrl(u)
            url = url.replace("[svn]", "")

            if url.find("://") == -1:
                sourcedir = CraftStandardDirs.svnDir() / url
            else:
                sourcedir = CraftStandardDirs.downloadDir() / "svn-src"
                sourcedir = sourcedir / self.package.path
                _, path = self.__splitPath(url)
                if path and CraftCore.settings.getboolean("General", "EMERGE_SVN_STDLAYOUT", False):
                    sourcedir = sourcedir / path
        else:
            CraftCore.log.critical("svnTarget property not set for this target")

        if self.subinfo.targetSourceSuffix() != None:
            sourcedir = "%s-%s" % (sourcedir, self.subinfo.targetSourceSuffix())

        return sourcedir

    def applyPatch(self, fileName, patchdepth, unusedSrcDir=None):
        """apply a patch to a svn repository checkout"""
        CraftCore.debug.trace("SvnSource.applyPatch")
        if fileName:
            return utils.applyPatch(self.sourceDir(), self.blueprintDir() / fileName, patchdepth)
        return True

    def fetch(self):
        """checkout or update an existing repository path"""
        CraftCore.debug.trace("SvnSource.fetch")
        if self.noFetch:
            CraftCore.log.debug("skipping svn fetch (--offline)")
            return True

        for i in range(self.repositoryUrlCount()):
            url = self.repositoryUrl(i)
            self.__tryCheckoutFromRoot(url, self.checkoutDir(i), self.repositoryUrlOptions(i) != "norecursive")
        return True

    def __getCurrentRevision(self):
        """return the revision returned by svn info"""

        revision = None

        # handle multiple urls in targets
        # we need to find the main url which is marked with #main
        # if not marked use the second last one, which is used currently
        sourcedir = None
        n = self.repositoryUrlCount()
        if n > 1:
            for i in range(0, n):
                if self.repositoryUrlOptions(i) == "main":
                    sourcedir = self.checkoutDir(i)
                    break
            # if not found use the second last one
            if sourcedir == None:
                sourcedir = self.checkoutDir(n - 2)
        else:
            sourcedir = self.checkoutDir()

        # set up the command
        cmd = "svn info %s" % (sourcedir)

        with tempfile.TemporaryFile() as tmp:

            # run the command
            env = os.environ.copy()
            env["LANG"] = "C"
            utils.system(cmd, stdout=tmp, env=env)

            tmp.seek(os.SEEK_SET)
            # read the temporary file and find the line with the revision
            for line in tmp:
                if line.startswith(b"Revision: "):
                    revision = str(line, "UTF-8").replace("Revision: ", "").strip()
                    break

        return revision

    def __splitPath(self, path):
        """split a path into a base part and a relative repository url.
        The delimiters are currently 'trunk', 'branches' and 'tags'.
        """
        pos = path.find("trunk")
        if pos == -1:
            pos = path.find("branches")
            if pos == -1:
                pos = path.find("tags")
        if pos == -1:
            ret = [path, None]
        else:
            ret = [path[: pos - 1], path[pos:]]
        return ret

    def __tryCheckoutFromRoot(self, url, sourcedir, recursive=True):
        """This method checkout source with svn informations from
        the svn root repository directory. It detects the svn root
        by searching the predefined root subdirectories 'trunk', 'branches'
        and 'tags' which will probably fit for most servers
        """
        (urlBase, urlPath) = self.__splitPath(url)
        if urlPath == None:
            return self.__checkout(url, sourcedir, recursive)

        (srcBase, srcPath) = self.__splitPath(sourcedir)
        if srcPath == None:
            return self.__checkout(url, sourcedir, recursive)

        urlRepo = urlBase
        srcDir = srcBase
        urlParts = urlPath.split("/")
        pathSep = "/"
        srcParts = srcPath.split(pathSep)

        # url and source parts not match
        if len(urlParts) != len(srcParts):
            return self.__checkout(url, sourcedir, recursive)

        for i in range(0, len(urlParts) - 1):
            urlPart = urlParts[i]
            srcPart = srcParts[i]
            if urlPart == "":
                continue

            urlRepo += "/" + urlPart
            srcDir += pathSep + srcPart

            if os.path.exists(srcDir):
                continue
            self.__checkout(urlRepo, srcDir, False)

        self.__checkout(url, sourcedir, recursive)

    def __checkout(self, url, sourcedir, recursive=True):
        """internal method for subversion checkout and update"""
        option = ""
        if not recursive:
            option = "--depth=files"

        if CraftCore.debug.verbose() < 2 and not CraftCore.settings.getboolean("General", "KDESVNVERBOSE", True):
            option += " --quiet"

        if self.subinfo.options.fetch.ignoreExternals:
            option += " --ignore-externals "

        url = utils.replaceVCSUrl(url)

        if os.path.exists(sourcedir):
            cmd = "svn update %s %s" % (option, sourcedir)
        else:
            cmd = "svn checkout %s %s %s" % (option, url, sourcedir)

        return utils.system(cmd)

    def createPatch(self):
        """create patch file from svn source into the related package dir. The patch file is named autocreated.patch"""
        cmd = "svn diff %s > %s" % (
            self.checkoutDir(),
            self.blueprintDir() / "%s-%s.patch" % (self.package, str(datetime.date.today()).replace("-", "")),
        )
        return utils.system(cmd)

    def sourceVersion(self):
        """print the revision returned by svn info"""
        return self.__getCurrentRevision()

    def getUrls(self):
        """print the url where to check out from"""
        for i in range(self.repositoryUrlCount()):
            url = self.repositoryUrl(i)
            if self.repositoryUrlOptions(i) == "norecursive":
                url = "--depth=files " + url
            print(url)
        return True
