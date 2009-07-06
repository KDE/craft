# -*- coding: utf-8 -*-

from Source.SourceBase import *
import utils

class ArchiveSource(SourceBase):
    """ file download source"""
    filenames = []    
    def __init__(self):
        SourceBase.__init__(self)
        utils.debug( "ArchiveSource.__init__ called", 1 )

    def __localFileNames(self):
        """ collect local filenames """
        utils.debug( "ArchiveSource.__localFileNames called", 1 )

        filenames =[]

        if self.subinfo.hasTarget():
            for uri in self.subinfo.target().split():
                filenames.append( os.path.basename( uri ) )
        return filenames

    def fetch(self):
        """getting normal tarballs from SRC_URI"""
        utils.debug( "ArchiveSource.fetch called", 1 )
            
        filenames = self.__localFileNames()
        
        if ( self.noFetch ):
            utils.debug( "skipping fetch (--offline)" )
            return True
        if self.subinfo.hasTarget():
            return utils.getFiles( self.subinfo.target(), self.downloaddir )
        else:
            return utils.getFiles( "", self.downloaddir )

    def unpack(self):
        """unpacking all zipped(gz,zip,bz2) tarballs"""        
        utils.debug( "ArchiveSource.unpack called", 1 )

        filenames = self.__localFileNames()        
        destdir = self.workDir()
        # if using BinaryBuildSystem the files should be unpacked into imagedir
        if hasattr(self, 'buildSystemType') and self.buildSystemType == 'binary':
            destdir = self.imageDir()
            utils.debug("unpacking files into image root %s" % destdir,1)
        else:
            utils.debug("unpacking files into work root %s" % destdir,1)

        if not utils.unpackFiles( self.downloaddir, filenames, destdir ):
            return False

        return self.applyPatches()

    def sourceDir(self): 
        sourcedir = self.workDir()
        if hasattr(self, 'buildSystemType') and self.buildSystemType == 'binary':
            sourcedir = self.imageDir()

        if self.subinfo.hasTargetSourcePath():
            sourcedir = os.path.join(sourcedir, self.subinfo.targetSourcePath())
        if utils.verbose > 1:
            print "using sourcedir: " + sourcedir
        return sourcedir

