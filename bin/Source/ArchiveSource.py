#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

import shutil

import EmergeDebug
from Source.SourceBase import *
import EmergeHash


class ArchiveSource(SourceBase):
    """ file download source"""
    filenames = []
    def __init__(self, subinfo=None):
        EmergeDebug.debug("ArchiveSource.__init__ called", 2)
        if subinfo:
            self.subinfo = subinfo
        SourceBase.__init__( self )

    def repositoryUrl(self, index=0):
        """all repository pathes"""
        if self.subinfo.hasTarget():
            return os.path.basename( self.subinfo.targetAt(index) )
        else:
            return False

    def repositoryUrlCount(self):
        return self.subinfo.targetCount()

    def localFileNames(self):
        # pylint: disable=E0202
        # but I have no idea why pylint thinks this overrides
        # MultiSource.localFileNames
        if self.subinfo.archiveName() == "":
            return self.localFileNamesBase()
        return self.subinfo.archiveName()

    def localFileNamesBase(self):
        """ collect local filenames """
        EmergeDebug.debug("ArchiveSource.localFileNamesBase called", 2)

        filenames = []
        for i in range(self.repositoryUrlCount()):
            filenames.append( os.path.basename( self.repositoryUrl( i ) ) )
        return filenames

    def __checkFilesPresent(self, filenames):
        """check if all files for the current target are available"""
        for filename in filenames:
            path = os.path.join(EmergeStandardDirs.downloadDir(), filename)
            if self.subinfo.hasTargetDigests():
                if not os.path.exists(path):
                    return False
            elif self.subinfo.hasTargetDigestUrls():
                algorithm = EmergeHash.HashAlgorithm.SHA1
                if  type(self.subinfo.targetDigestUrl()) == tuple:
                    _, algorithm = self.subinfo.targetDigestUrl()
                if not os.path.exists(path + algorithm.fileEnding()):
                    return False
            elif not os.path.exists(path):
                return False
        return True

    def fetch( self, dummyRepopath = None ):
        """fetch normal tarballs"""
        EmergeDebug.debug("ArchiveSource.fetch called", 2)

        filenames = self.localFileNames()

        if ( self.noFetch ):
            EmergeDebug.debug("skipping fetch (--offline)")
            return True

        self.setProxy()
        if self.subinfo.hasTarget():
            if self.__checkFilesPresent(filenames):
                EmergeDebug.debug("files and digests available, no need to download files", 1)
                return True

            result = utils.getFiles( self.subinfo.target(), EmergeStandardDirs.downloadDir() , filenames = self.subinfo.archiveName() )
            if not result:
                EmergeDebug.debug("failed to download files", 1)
                return False
            if result and self.subinfo.hasTargetDigestUrls():
                if type(self.subinfo.targetDigestUrl()) == tuple:
                    url, alg = self.subinfo.targetDigestUrl()
                    return utils.getFiles(url, EmergeStandardDirs.downloadDir(),
                                          filenames = self.subinfo.archiveName()
                                                        + EmergeHash.HashAlgorithm.fileEndings().get(alg))
                else:
                    return utils.getFiles( self.subinfo.targetDigestUrl(), EmergeStandardDirs.downloadDir(), filenames = '' )
            else:
                EmergeDebug.debug("no digestUrls present", 2)
                return True
        else:
            return utils.getFiles( "", EmergeStandardDirs.downloadDir() )

    def checkDigest(self):
        EmergeDebug.debug("ArchiveSource.checkDigest called", 2)
        filenames = self.localFileNames()

        if self.subinfo.hasTargetDigestUrls():
            EmergeDebug.debug("check digests urls", 1)
            if not EmergeHash.checkFilesDigests(EmergeStandardDirs.downloadDir(), filenames):
                EmergeDebug.error("invalid digest file")
                return False
        elif self.subinfo.hasTargetDigests():
            EmergeDebug.debug("check digests", 1)
            digests = self.subinfo.targetDigest()
            algorithm = EmergeHash.HashAlgorithm.SHA1
            if type(digests) == tuple:
                digests, algorithm = digests
            if not EmergeHash.checkFilesDigests( EmergeStandardDirs.downloadDir(), filenames, digests, algorithm):
                EmergeDebug.error("invalid digest file")
                return False
        else:
            EmergeDebug.debug("print source file digests", 1)
            EmergeHash.printFilesDigests(EmergeStandardDirs.downloadDir(), filenames, self.subinfo.buildTarget, algorithm = EmergeHash.HashAlgorithm.SHA256)
        return True

    def unpack(self):
        """unpacking all zipped(gz, zip, bz2) tarballs"""
        EmergeDebug.debug("ArchiveSource.unpack called", 2)

        filenames = self.localFileNames()

        destdir = self.sourceDir()
        # self.sourceDir() will already contain targetInstSrc so we have to remove it
        if self.subinfo.hasTargetSourcePath():
            destdir = destdir[:-len(self.subinfo.targetSourcePath())]
        utils.cleanDirectory(destdir)

        if hasattr(self.subinfo.options.unpack, 'unpackDir'):
            destdir = os.path.join(destdir, self.subinfo.options.unpack.unpackDir)

        self.checkDigest()



        binEndings = (".exe", ".bat", ".msi")
        for filename in filenames:
            if filename.endswith(binEndings):
                filePath = os.path.abspath( os.path.join(EmergeStandardDirs.downloadDir(), filename) )
                if self.subinfo.options.unpack.runInstaller: 
                    _, ext = os.path.splitext( filename )
                    if ext == ".exe":
                        return utils.system("%s" % filePath )
                    elif ( ext == ".msi" ):
                        return utils.system("msiexec /package %s" % filePath )
                if not utils.copyFile( filePath, os.path.join(destdir, filename) ):
                    return False
            else:
                if not utils.unpackFile( EmergeStandardDirs.downloadDir(), filename, destdir ):
                    return False

        ret = self.applyPatches()
        if emergeSettings.getboolean("General","EMERGE_HOLD_ON_PATCH_FAIL",False):
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
            EmergeDebug.die("could not find diff tool, please run 'emerge diffutils'")
        
        # get the file paths of the tarballs
        filenames = self.localFileNames()

        destdir = self.workDir()

        # it makes no sense to make a diff against nothing
        if ( not os.path.exists( self.sourceDir() ) ):
            EmergeDebug.error("source directory doesn't exist, please run unpack first")
            return False

        EmergeDebug.debug("unpacking files into work root %s" % destdir, 1)


        # make a temporary directory so the original packages don't overwrite the already existing ones
        tmpdir = os.path.join( destdir, "tmp" )
        unpackDir = tmpdir

        utils.cleanDirectory( unpackDir )

        if ( not os.path.exists( unpackDir ) ):
            os.mkdir( unpackDir )

        if hasattr( self.subinfo.options.unpack, 'unpackDir' ):
            unpackDir = os.path.join( unpackDir, self.subinfo.options.unpack.unpackDir )

            if ( not os.path.exists( unpackDir ) ):
                os.mkdir( unpackDir )

        # unpack all packages
        for filename in filenames:
            EmergeDebug.debug("unpacking this file: %s" % filename, 1)
            if ( not utils.unpackFile( EmergeStandardDirs.downloadDir(), filename, unpackDir ) ):
                return False

        packagelist = os.listdir( tmpdir )

        # apply all patches only ommitting the last one, this makes it possible to always work on the latest patch
        # for future work, it might be interesting to switch patches on and off at will, this probably needs an
        # own patch management though
        patchName = None
        if self.subinfo.hasTarget() or self.subinfo.hasSvnTarget():
            patches = self.subinfo.patchesToApply()
            if not isinstance(patches, list):
                patches = list([patches])
            for fileName, patchdepth in patches[:-1]:
                EmergeDebug.debug("applying patch %s with patchlevel: %s" % (fileName, patchdepth))
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

        EmergeDebug.debug("patch created at %s" % patchName)
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
