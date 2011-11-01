#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

from Source.SourceBase import *
import shutil

class ArchiveSource(SourceBase):
    """ file download source"""
    filenames = []
    def __init__(self, subinfo=None):
        utils.debug( "ArchiveSource.__init__ called", 2 )
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
        return  self.subinfo.archiveName()

    def localFileNamesBase(self):
        """ collect local filenames """
        utils.debug( "ArchiveSource.localFileNamesBase called", 2 )

        filenames = []
        for i in range(self.repositoryUrlCount()):
            filenames.append( os.path.basename( self.repositoryUrl( i ) ) )
        return filenames

    def __checkFilesPresent(self, filenames):
        """check if all files for the current target are available"""
        available = True
        for filename in filenames:
            path = os.path.join(self.downloadDir(), filename)
            if self.subinfo.hasTargetDigests():
                if not os.path.exists(path):
                    available = False
            elif self.subinfo.hasTargetDigestUrls():
                if not os.path.exists("%s.sha1" % path):
                    available = False
            elif not os.path.exists(path):
                available = False
        return available

    def fetch( self, dummyRepopath = None ):
        """fetch normal tarballs"""
        utils.debug( "ArchiveSource.fetch called", 2 )

        filenames = self.localFileNames()

        if ( self.noFetch ):
            utils.debug( "skipping fetch (--offline)" )
            return True

        self.setProxy()
        if self.subinfo.hasTarget():
            if self.__checkFilesPresent(filenames):
                utils.debug("files and digests available, no need to download files", 1)
                return True

            result = utils.getFiles( self.subinfo.target(), self.downloadDir() , filenames = self.subinfo.archiveName() )
            if not result:
                return False
            if result and self.subinfo.hasTargetDigestUrls():
                if self.subinfo.targetDigestUrl() == "auto":
                    return utils.getFiles( self.subinfo.target(), self.downloadDir(), ".sha1", self.subinfo.archiveName() )
                else:
                    return utils.getFiles( self.subinfo.targetDigestUrl(), self.downloadDir() ,filenames = self.subinfo.archiveName() )
            else:
                return True
        else:
            return utils.getFiles( "", self.downloadDir() )

    def checkDigest(self):
        utils.debug( "ArchiveSource.checkDigest called", 2 )
        filenames = self.localFileNames()

        if self.subinfo.hasTargetDigestUrls():
            utils.debug("check digests urls", 1)
            if not utils.checkFilesDigests( self.downloadDir(), filenames):
                utils.error("invalid digest file")
                return False
        elif self.subinfo.hasTargetDigests():
            utils.debug("check digests", 1)
            if not utils.checkFilesDigests( self.downloadDir(), filenames, self.subinfo.targetDigest()):
                utils.error("invalid digest file")
                return False
        else:
            utils.debug("print source file digests", 1)
            digests = utils.createFilesDigests( self.downloadDir(), filenames )
            utils.printFilesDigests( digests, self.subinfo.buildTarget)
        return True

    def unpack(self):
        """unpacking all zipped(gz, zip, bz2) tarballs"""
        utils.debug( "ArchiveSource.unpack called", 2 )

        filenames = self.localFileNames()
        ## @todo: unpack destination is probably sourceDir()
        # unfortunally subinfo.targetInstSrc attribute is only for accessing a source subdir
        # for unpacking into a subdir we need an additional property

        # if using BinaryBuildSystem the files should be unpacked into imagedir
        if self.buildSystemType == 'binary':
            destdir = self.installDir()
            utils.debug("unpacking files into image root %s" % destdir, 1)
        # tempory solution
        elif self.subinfo.options.unpack.unpackIntoBuildDir:
            destdir = self.buildDir()
            utils.debug("unpacking files into build dir %s" % destdir, 1)
        else:
            destdir = self.workDir()
            utils.debug("unpacking files into work root %s" % destdir, 1)

        if hasattr(self.subinfo.options.unpack, 'unpackDir'):
            destdir = os.path.join(destdir, self.subinfo.options.unpack.unpackDir)

        if self.subinfo.hasTargetDigestUrls():
            utils.debug("check digests urls", 1)
            if not utils.checkFilesDigests( self.downloadDir(), filenames):
                utils.error("invalid digest file")
                return False
        elif self.subinfo.hasTargetDigests():
            utils.debug("check digests", 1)
            if not utils.checkFilesDigests( self.downloadDir(), filenames, self.subinfo.targetDigest()):
                utils.error("invalid digest file")
                return False
        else:
            utils.debug("print source file digests", 1)
            digests = utils.createFilesDigests( self.downloadDir(), filenames )
            utils.printFilesDigests( digests, self.subinfo.buildTarget)

        if not utils.unpackFiles( self.downloadDir(), filenames, destdir ):
            return False

        ret = self.applyPatches()
        if utils.envAsBool("EMERGE_HOLD_ON_PATCH_FAIL"):
            return ret
        return True

    def getUrls( self ):
        print self.subinfo.target()
        print self.subinfo.targetDigestUrl()
        return True

    def createPatch( self ):
        """ unpacking all zipped(gz, zip, bz2) tarballs a second time and making a patch """
        
        diffExe = os.path.join( self.rootdir, "dev-utils", "bin", "diff.exe" )
        if not os.path.exists( diffExe ):
            utils.die("could not find diff tool, please run 'emerge diffutils'")
        
        # get the file paths of the tarballs
        filenames = self.localFileNames()

        # if using BinaryBuildSystem the files should be unpacked into imagedir
        if self.buildSystemType == 'binary':
            destdir = self.installDir()
            utils.debug( "unpacking files into image root %s" % destdir, 1 )
        else:
            destdir = self.workDir()

        # it makes no sense to make a diff against nothing
        if ( not os.path.exists( self.sourceDir() ) ):
            utils.error( "source directory doesn't exist, please run unpack first" )
            return False

        utils.debug( "unpacking files into work root %s" % destdir, 1 )


        # make a temporary directory so the original packages don't overwrite the already existing ones
        tmpdir = os.path.join( destdir, "tmp" )
        unpackDir = tmpdir

        if ( not os.path.exists( unpackDir ) ):
            os.mkdir( unpackDir )

        if hasattr( self.subinfo.options.unpack, 'unpackDir' ):
            unpackDir = os.path.join( unpackDir, self.subinfo.options.unpack.unpackDir )

            if ( not os.path.exists( unpackDir ) ):
                os.mkdir( unpackDir )

        # unpack all packages
        for filename in filenames:
            utils.debug( "unpacking this file: %s" % filename, 1 )
            if ( not utils.unpackFile( self.downloadDir(), filename, unpackDir ) ):
                return False

        packagelist = os.listdir( tmpdir )

        # apply all patches only ommitting the last one, this makes it possible to always work on the latest patch
        # for future work, it might be interesting to switch patches on and off at will, this probably needs an
        # own patch management though
        if self.subinfo.hasTarget() or self.subinfo.hasSvnTarget():
            patches = self.subinfo.patchesToApply()
            if type(patches) == list:
                # TODO: I seem to remember this is not good, prefer isinstance(patches, list)
                # have to check back. Maybe because this does not work with derived classes
                for fileName, patchdepth in patches[:-1]:
                    utils.debug( "applying patch %s with patchlevel: %s" % ( fileName, patchdepth ) )
                    if not self.applyPatch( fileName, patchdepth, os.path.join( tmpdir, packagelist[ 0 ] ) ):
                        return False

        # move the packages up and rename them to be different from the original source directory
        for directory in packagelist:
            # if the source or dest directory already exists, remove the occurance instead
            if os.path.exists( os.path.join( destdir, directory + ".orig" ) ):
                shutil.rmtree( os.path.join( destdir, directory + ".orig" ) )
            shutil.move( os.path.join( tmpdir, directory ), os.path.join( destdir, directory + ".orig" ) )

        # make one diff per file, even though we aren't able to apply multiple patches per package atm
        os.chdir( destdir )
        for directory in packagelist:
            outFile = os.path.join( self.buildRoot(), "%s-%s.diff" % ( directory, \
                str( datetime.date.today() ).replace('-', '') ) )
            cmd = "diff -Nru %s.orig %s > %s || echo 0" % ( directory, directory, outFile )
            if not self.system( cmd ):
                return False

        utils.debug( "patch created at %s" % outFile )
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
        print self.subinfo.buildTarget
        return True
