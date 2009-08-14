# 
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

from Source.SourceBase import *
import utils

class FileSource(SourceBase):
    """ file download source"""
    filenames = []    
    def __init__(self):
        utils.debug( "FileSource.__init__ called", 2 )
        SourceBase.__init__(self)

    def __localFileNames(self):
        """ collect local filenames """
        utils.debug( "FileSource.__localFileNames called", 2 )

        filenames =[]

        if self.subinfo.hasTarget():
            for uri in self.subinfo.target().split():
                filenames.append( os.path.basename( uri ) )
        return filenames

    def fetch(self):
        """fetching binary files"""
        utils.debug( "FileSource.fetch called", 2 )
            
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
        """copying files into local dir"""        
        utils.debug( "FileSource.unpack called", 2 )

        filenames = self.__localFileNames()        
        # if using BinaryBuildSystem the files should be unpacked into imagedir
        if hasattr(self, 'buildSystemType') and self.buildSystemType == 'binary':
            destdir = self.installDir()
            if not os.path.exists(destdir):
                os.makedirs(destdir)
            utils.debug("unpacking files into image root %s" % destdir,1)
        else:
            destdir = self.workDir()
            self.enterBuildDir()
            utils.debug("unpacking files into work root %s" % destdir,1)

        for filename in filenames:
            if not utils.copyFile( os.path.join(self.downloadDir(), filename),  os.path.join(destdir,filename) ):
                return False
        return True
