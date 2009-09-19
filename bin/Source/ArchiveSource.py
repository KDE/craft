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

    def __localFileNames(self):
        """ collect local filenames """
        utils.debug( "ArchiveSource.__localFileNames called", 2 )

        filenames =[]

        if self.subinfo.hasTarget():
            for uri in self.subinfo.target().split():
                filenames.append( os.path.basename( uri ) )
        return filenames

                    
    def fetch(self):
        """getting normal tarballs from SRC_URI"""
        utils.debug( "ArchiveSource.fetch called", 2 )
            
        filenames = self.__localFileNames()
        
        if ( self.noFetch ):
            utils.debug( "skipping fetch (--offline)" )
            return True

        self.setProxy()
        if self.subinfo.hasTarget():
            return utils.getFiles( self.subinfo.target(), self.downloadDir() )
        else:
            return utils.getFiles( "", self.downloadDir() )

    def unpack(self):
        """unpacking all zipped(gz,zip,bz2) tarballs"""        
        utils.debug( "ArchiveSource.unpack called", 2 )

        filenames = self.__localFileNames()        
        # if using BinaryBuildSystem the files should be unpacked into imagedir
        if hasattr(self, 'buildSystemType') and self.buildSystemType == 'binary':
            destdir = self.installDir()
            utils.debug("unpacking files into image root %s" % destdir,1)
        else:
            destdir = self.workDir()
            
            if ( not os.path.exists( self.buildDir()) ):
                os.makedirs( self.buildDir() )
                utils.debug( "creating: %s" % self.buildDir(), 0 )

            utils.debug("unpacking files into work root %s" % destdir,1)

        if not utils.unpackFiles( self.downloadDir(), filenames, destdir ):
            return False

        return self.applyPatches()

    def createPatch( self ):
        """ unpacking all zipped(gz,zip,bz2) tarballs a second time and making a patch """
        # get the file paths of the tarballs
        filenames = self.__localFileNames()

        # if using BinaryBuildSystem the files should be unpacked into imagedir
        if hasattr( self, 'buildSystemType' ) and self.buildSystemType == 'binary':
            destdir = self.installDir()
            utils.debug( "unpacking files into image root %s" % destdir, 1 )
        else:
            destdir = self.workDir()

        # it makes no sense to make a diff against nothing
        if ( not os.path.exists( self.buildDir() ) ):
            utils.error( "build directory doesn't exist, please run unpack first" )
            return False

        utils.debug( "unpacking files into work root %s" % destdir, 1 )


        # make a temporary directory so the original packages don't overwrite the already existing ones
        tmpdir = os.path.join( destdir, "tmp" )
        if ( not os.path.exists( tmpdir ) ):
            os.mkdir( tmpdir )

        # unpack all packages
        for filename in filenames:
            utils.debug( "unpacking this file: %s" % filename, 1 )
            if ( not utils.unpackFile( self.downloadDir(), filename, tmpdir ) ):
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