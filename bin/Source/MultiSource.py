# 
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

import info
import utils

from SourceFactory import *

class MultiSource(object):
    """ provides multi source type api """
    def __init__(self):
        object.__init__(self)
        utils.trace( "MultiSource __init__", 2 )
        self.source = SourceFactory(self.subinfo)
        self.source.localFileNames = self.localFileNames.__get__(self, MultiSource)
        self.source.category = self.category
        self.source.package = self.package
        self.source.version = self.version
        self.source.PV = self.PV

    def localFileNames( self ):
        utils.trace( "MultiSource localFileNames", 2 )
        return self.source.localFileNamesBase()

    def fetch(self):
        utils.trace( "MultiSource fetch", 2 )
        return self.source.fetch()
        
    def checkDigest(self):
        utils.trace( "MultiSource checkDigest", 2 )
        return self.source.checkDigest()

    def unpack(self):
        utils.trace( "MultiSource unpack", 2 )
        self.source.buildSystemType = self.buildSystemType
        return self.source.unpack()

    def sourceDir(self):
        utils.trace( "MultiSource sourceDir", 2 )
        return self.source.sourceDir()

    def repositoryUrl(self,index=0):
        utils.trace( "MultiSource repositoryUrl", 2 )
        return self.source.repositoryUrl(index)

    def repositoryUrlCount(self):
        utils.trace( "MultiSource repositoryUrlCount", 2 )
        return self.source.repositoryUrlCount()

    def applyPatches(self):
        utils.trace( "MultiSource applyPatches", 2 )
        return self.source.applyPatches()

    def applyPatch(self):
        utils.trace( "MultiSource applyPatch", 2 )
        return self.source.applyPatch()

    def createPatch(self):
        utils.trace( "MultiSource createPatch", 2 )
        return self.source.createPatch()
        
    def sourceVersion(self):
        utils.trace( "MultiSource sourceVersion", 2 )
        return self.source.sourceVersion()
