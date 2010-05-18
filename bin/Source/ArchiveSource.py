# 
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

from Source.SourceBase import *
import utils
import shutil

class ArchiveSource(SourceBase):
    """ file download source"""
    filenames = []    
    def __init__(self):
        utils.debug( "ArchiveSource.__init__ called", 2 )
        SourceBase.__init__(self)

    def repositoryUrl(self, index=0):
        """all repository pathes"""
        if self.subinfo.hasTarget():
            return os.path.basename( self.subinfo.target().split()[index] )
        else:
            return False
        
    def repositoryUrlCount(self):
        return len( self.subinfo.target().split() )

    def localFileNames(self):
        return self.localFileNamesBase()

    def localFileNamesBase( self):
        """ collect local filenames """
        utils.debug( "ArchiveSource.localFileNamesBase called", 2 )

        filenames = []
        for i in range(self.repositoryUrlCount()):
            filenames.append( os.path.basename( self.repositoryUrl( i ) ) )
        return filenames

    def __checkFilesPresent(self,filenames):
        """check if all files for the current target are available"""
        available = True
        for filename in filenames:
            path =os.path.join(self.downloadDir(), filename)
            if self.subinfo.hasTargetDigests():
                if not os.path.exists(path):
                    available = False    
            elif self.subinfo.hasTargetDigestUrls(): 
                if not os.path.exists("%s.sha1" % path):
                    available = False    
            elif not os.path.exists(path):
                available = False    
        return available

    def fetch(self):
        """getting normal tarballs from SRC_URI"""
        utils.debug( "ArchiveSource.fetch called", 2 )
            
        filenames = self.localFileNames()

        if ( self.noFetch ):
            utils.debug( "skipping fetch (--offline)" )
            return True

        self.setProxy()
        if self.subinfo.hasTarget():
            if self.__checkFilesPresent(filenames):
                utils.debug("files and digests available, no need to download files",1)
                return True

            result = utils.getFiles( self.subinfo.target(), self.downloadDir() )
            if not result: 
                return False
            if result and self.subinfo.hasTargetDigestUrls():
                if self.subinfo.targetDigestUrl() == "auto":
                    return utils.getFiles( self.subinfo.target(), self.downloadDir(), ".sha1" )
                else:
                    return utils.getFiles( self.subinfo.targetDigestUrl(), self.downloadDir() )
            else:
                return True
        else:
            return utils.getFiles( "", self.downloadDir() )

    def unpack(self):
        """unpacking all zipped(gz,zip,bz2) tarballs"""        
        utils.debug( "ArchiveSource.unpack called", 2 )

        filenames = self.localFileNames()
        ## @todo: unpack destination is probably sourceDir()
        # unfortunally subinfo.targetInstSrc attribute is only for accessing a source subdir
        # for unpacking into a subdir we need an additional property
        
        # if using BinaryBuildSystem the files should be unpacked into imagedir
        if hasattr(self, 'buildSystemType') and self.buildSystemType == 'binary':
            destdir = self.installDir()
            utils.debug("unpacking files into image root %s" % destdir,1)
        # tempory solution
        elif self.subinfo.options.unpack.unpackIntoBuildDir:
            destdir = self.buildDir()
            utils.debug("unpacking files into build dir %s" % destdir,1)
        else:
            destdir = self.workDir()
            utils.debug("unpacking files into work root %s" % destdir,1)

        if hasattr(self.subinfo.options.unpack, 'unpackDir'):
            destdir = os.path.join(destdir, self.subinfo.options.unpack.unpackDir)

        if self.subinfo.hasTargetDigestUrls():
            utils.debug("check digests urls",1)
            if not utils.checkFilesDigests( self.downloadDir(), filenames):
                utils.error("invalid digest file")
                return False
        elif self.subinfo.hasTargetDigests():
            utils.debug("check digests",1)
            if not utils.checkFilesDigests( self.downloadDir(), filenames, self.subinfo.targetDigest()):
                utils.error("invalid digest file")
                return False
        else: 
            utils.debug("print source file digests",1)
            digests = utils.createFilesDigests( self.downloadDir(), filenames )
            utils.printFilesDigests( digests,self.subinfo.buildTarget)

        if not utils.unpackFiles( self.downloadDir(), filenames, destdir ):
            return False

        return self.applyPatches()

    def createPatch( self ):
        """ unpacking all zipped(gz,zip,bz2) tarballs a second time and making a patch """
        # get the file paths of the tarballs
        filenames = self.localFileNames()

        # if using BinaryBuildSystem the files should be unpacked into imagedir
        if hasattr( self, 'buildSystemType' ) and self.buildSystemType == 'binary':
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
        
        # move the packages up and rename them to be different from the original source directory
        for dir in packagelist:
            # if the source or dest directory already exists, remove the occurance instead
            if os.path.exists( os.path.join( destdir, dir + ".orig" ) ):
                shutil.rmtree( os.path.join( destdir, dir + ".orig" ) )
            shutil.move( os.path.join( tmpdir, dir ), os.path.join( destdir, dir + ".orig" ) )

        # make one diff per file, even though we aren't able to apply multiple patches per package atm
        os.chdir( destdir )
        for dir in packagelist:
            cmd = "diff -Nru %s.orig %s > %s || echo 0" % ( dir, dir, os.path.join( self.buildRoot(), \
            "%s-%s.diff" % ( dir, str( datetime.date.today() ).replace('-', '') ) ) )
            if not self.system( cmd ):
                return False
            
        # remove all directories that are not needed any more after making the patch
        # disabled for now
        #for dir in packagelist:
        #    shutil.rmtree( dir + ".orig" )
            
        # remove the temporary directory, it should be empty after all directories have been moved up
        os.rmdir( tmpdir )

        return True
        
    def sourceVersion( self ):
        """ return a version based on the file name of the current target """
        # we hope that the build target is equal to the version that is build
        print self.subinfo.buildTarget
        return True