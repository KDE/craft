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

        if self.subinfo.buildTarget in self.subinfo.targets.keys(): # and not self.repoPath():
            filenames = []
            for uri in self.subinfo.targets[ self.subinfo.buildTarget ].split():
                filenames.append( os.path.basename( uri ) )
        return filenames

    def fetch(self):
        """getting normal tarballs from SRC_URI"""
        utils.debug( "ArchiveSource.fetch called", 1 )
            
        filenames = self.__localFileNames()
        
        if ( self.noFetch ):
            utils.debug( "skipping fetch (--offline)" )
            return True
        if len( self.subinfo.targets ) and self.subinfo.buildTarget in self.subinfo.targets.keys():
            return utils.getFiles( self.subinfo.targets[ self.subinfo.buildTarget ], self.downloaddir )
        else:
            return utils.getFiles( "", self.downloaddir )

    def unpack(self):
        """unpacking all zipped(gz,zip,bz2) tarballs"""        
        utils.debug( "ArchiveSource.unpack called", 1 )

        filenames = self.__localFileNames()        
        if not utils.unpackFiles( self.downloaddir, filenames, self.imagedir ):
            return False

        return self.applyPatches()
