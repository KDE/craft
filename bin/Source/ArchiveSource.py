#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

import os
import shutil

from CraftDebug import craftDebug
from Source.SourceBase import *
import CraftHash


class ArchiveSource(SourceBase):
    """ file download source"""
    def __init__(self):
        craftDebug.log.debug("ArchiveSource.__init__ called")
        SourceBase.__init__( self )

    def localFileNames(self):
        if self.subinfo.archiveName() == [""]:
            return self.localFileNamesBase()
        if isinstance(self.subinfo.archiveName(), (tuple,list)):
            return self.subinfo.archiveName()
        return [self.subinfo.archiveName()]

    def localFileNamesBase(self):
        """ collect local filenames """
        craftDebug.log.debug("ArchiveSource.localFileNamesBase called")

        filenames = []
        for url in self.subinfo.targets.values():
            filenames.append( os.path.basename( url ) )
        return filenames

    def __checkFilesPresent(self, filenames):
        def isFileValid(path):
            if not os.path.exists(path):
                return False

            return os.path.getsize(path) > 0

        """check if all files for the current target are available"""
        for filename in filenames:
            path = os.path.join(CraftStandardDirs.downloadDir(), filename)

            # check file
            if not isFileValid(path):
                return False

            # check digests
            if self.subinfo.hasTargetDigests():
                if not isFileValid(path):
                    return False
            elif self.subinfo.hasTargetDigestUrls():
                algorithm = CraftHash.HashAlgorithm.SHA1
                if  type(self.subinfo.targetDigestUrl()) == tuple:
                    _, algorithm = self.subinfo.targetDigestUrl()
                if not isFileValid(path + algorithm.fileEnding()):
                    return False
        return True

    def fetch( self, dummyRepopath = None ):
        """fetch normal tarballs"""
        craftDebug.log.debug("ArchiveSource.fetch called")

        filenames = self.localFileNames()

        if ( self.noFetch ):
            craftDebug.log.debug("skipping fetch (--offline)")
            return True

        self.setProxy()
        if self.subinfo.hasTarget():
            if self.__checkFilesPresent(filenames):
                craftDebug.log.debug("files and digests available, no need to download files")
                return True

            result = utils.getFiles( self.subinfo.target(), CraftStandardDirs.downloadDir() , filenames = self.subinfo.archiveName() )
            if not result:
                craftDebug.log.debug("failed to download files")
                return False
            if result and self.subinfo.hasTargetDigestUrls():
                if type(self.subinfo.targetDigestUrl()) == tuple:
                    url, alg = self.subinfo.targetDigestUrl()
                    return utils.getFiles(url, CraftStandardDirs.downloadDir(),
                                          filenames = self.subinfo.archiveName()[0]
                                                        + CraftHash.HashAlgorithm.fileEndings().get(alg))
                else:
                    return utils.getFiles( self.subinfo.targetDigestUrl(), CraftStandardDirs.downloadDir(), filenames = '' )
            else:
                craftDebug.log.debug("no digestUrls present")
                return True
        else:
            return utils.getFiles( "", CraftStandardDirs.downloadDir() )

    def checkDigest(self):
        craftDebug.log.debug("ArchiveSource.checkDigest called")
        filenames = self.localFileNames()

        if self.subinfo.hasTargetDigestUrls():
            craftDebug.log.debug("check digests urls")
            if not CraftHash.checkFilesDigests(CraftStandardDirs.downloadDir(), filenames):
                craftDebug.log.error("invalid digest file")
                return False
        elif self.subinfo.hasTargetDigests():
            craftDebug.log.debug("check digests")
            digests, algorithm = self.subinfo.targetDigest()
            if not CraftHash.checkFilesDigests( CraftStandardDirs.downloadDir(), filenames, digests, algorithm):
                craftDebug.log.error("invalid digest file")
                return False
        else:
            craftDebug.log.debug("print source file digests")
            CraftHash.printFilesDigests(CraftStandardDirs.downloadDir(), filenames, self.subinfo.buildTarget, algorithm = CraftHash.HashAlgorithm.SHA256)
        return True

    def unpack(self):
        """unpacking all zipped(gz, zip, bz2) tarballs"""
        craftDebug.log.debug("ArchiveSource.unpack called")

        filenames = self.localFileNames()

        # TODO: this might delete generated patches
        utils.cleanDirectory(self.workDir())

        if not self.checkDigest():
            return False

        binEndings = (".exe", ".bat", ".msi")
        for filename in filenames:
            if filename.endswith(binEndings):
                filePath = os.path.abspath( os.path.join(CraftStandardDirs.downloadDir(), filename) )
                if self.subinfo.options.unpack.runInstaller:
                    _, ext = os.path.splitext( filename )
                    if ext == ".exe":
                        return utils.system("%s %s" % (filePath, self.subinfo.options.configure.defines ))
                    elif ( ext == ".msi" ):
                        return utils.system("msiexec /package %s %s" % (filePath, self.subinfo.options.configure.defines) )
                if not utils.copyFile( filePath, os.path.join(self.workDir(), filename) ):
                    return False
            else:
                if not utils.unpackFile( CraftStandardDirs.downloadDir(), filename, self.workDir()):
                    return False

        ret = self.applyPatches()
        if craftSettings.getboolean("General","EMERGE_HOLD_ON_PATCH_FAIL",False):
            return ret
        return True

    def getUrls( self ):
        print(self.subinfo.target())
        print(self.subinfo.targetDigestUrl())
        return True

    def createPatch( self ):
        """ unpacking all zipped(gz, zip, bz2) tarballs a second time and making a patch """

        diffExe = os.path.join( self.rootdir, "dev-utils", "bin", "diff.exe" )
        if not os.path.exists( diffExe ):
            craftDebug.log.critical("could not find diff tool, please run 'craft diffutils'")

        # get the file paths of the tarballs
        filenames = self.localFileNames()

        destdir = self.workDir()

        # it makes no sense to make a diff against nothing
        if ( not os.path.exists( self.sourceDir() ) ):
            craftDebug.log.error("source directory doesn't exist, please run unpack first")
            return False

        craftDebug.log.debug("unpacking files into work root %s" % destdir)


        # make a temporary directory so the original packages don't overwrite the already existing ones
        tmpdir = os.path.join( destdir, "tmp" )
        unpackDir = tmpdir

        utils.cleanDirectory( unpackDir )

        if ( not os.path.exists( unpackDir ) ):
            os.mkdir( unpackDir )

            if ( not os.path.exists( unpackDir ) ):
                os.mkdir( unpackDir )

        # unpack all packages
        for filename in filenames:
            craftDebug.log.debug("unpacking this file: %s" % filename)
            if ( not utils.unpackFile( CraftStandardDirs.downloadDir(), filename, unpackDir ) ):
                return False

        packagelist = os.listdir( tmpdir )

        # apply all patches only ommitting the last one, this makes it possible to always work on the latest patch
        # for future work, it might be interesting to switch patches on and off at will, this probably needs an
        # own patch management though
        patchName = None
        if self.subinfo.hasTarget() or self.subinfo.hasSvnTarget():
            patches = self.subinfo.patchesToApply()
            if not isinstance(patches, list):
                patches = [patches]
            for fileName, patchdepth in patches[:-1]:
                craftDebug.log.debug("applying patch %s with patchlevel: %s" % (fileName, patchdepth))
                if not self.applyPatch( fileName, patchdepth, os.path.join( tmpdir, packagelist[ 0 ] ) ):
                    return False
            if patches[-1][0]:
                patchName = os.path.join( self.buildRoot(), patches[-1][0] )

        # move the packages up and rename them to be different from the original source directory
        for directory in packagelist:
            # if the source or dest directory already exists, remove the occurance instead
            if os.path.exists( os.path.join( destdir, directory + ".orig" ) ):
                shutil.rmtree( os.path.join( destdir, directory + ".orig" ) )
            shutil.move( os.path.join( tmpdir, directory ), os.path.join( destdir, directory + ".orig" ) )

        os.chdir( destdir )
        for directory in packagelist:
            if not patchName:
                patchName = os.path.join( self.buildRoot(), "%s-%s.diff" % ( directory, \
                str( datetime.date.today() ).replace('-', '') ) )
            cmd = "diff -Nrub -x *~ -x *\.rej -x *\.orig -x*\.o %s.orig %s > %s || echo 0" % ( directory, directory, patchName )
            if not self.system( cmd ):
                return False

        craftDebug.log.debug("patch created at %s" % patchName)
        # remove all directories that are not needed any more after making the patch
        # disabled for now
        #for directory in packagelist:
        #    shutil.rmtree( directory + ".orig" )

        # remove the temporary directory, it should be empty after all directories have been moved up
        os.rmdir( tmpdir )

        return True

    def sourceVersion( self ):
        """ return a version based on the file name of the current target """
        # we hope that the build target is equal to the version that is build
        return self.subinfo.buildTarget
