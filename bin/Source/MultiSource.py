# 
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

import info
import utils

from SourceFactory import *

class MultiSource():
    """ provides multi source type api """
    def __init__(self):
        utils.debug( "MultiSource __init__", 2 )

        self.source = SourceFactory(self.subinfo)
        self.source.category = self.category
        self.source.package = self.package
        self.source.version = self.version
        self.source.PV = self.PV

    def fetch(self):
        return self.source.fetch()
        
    def unpack(self):
        self.source.buildSystemType = self.buildSystemType
        return self.source.unpack()

    def sourceDir(self):
        return self.source.sourceDir()

    def repositoryPath(self):
        return self.source.repositoryPath()
        
    def applyPatches(self):
        return self.source.applyPatches()
