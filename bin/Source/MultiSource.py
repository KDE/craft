#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
from CraftDebug import craftDebug
import utils

from Source.SourceFactory import *

class MultiSource(object):
    """ provides multi source type api """
    def __init__(self):
        object.__init__(self)
        craftDebug.trace("MultiSource __init__")
        self.source = SourceFactory(self.subinfo)
        self.source.localFileNames = self.localFileNames.__get__(self, MultiSource)


    def localFileNames( self ):
        craftDebug.trace("MultiSource localFileNames")
        if self.subinfo.archiveName() == "":
            return self.source.localFileNamesBase()
        if isinstance(self.subinfo.archiveName(), (list, tuple)):
            return self.subinfo.archiveName()
        else:
            return (self.subinfo.archiveName(), )

    def fetch(self):
        craftDebug.trace("MultiSource fetch")
        return self.source.fetch()

    def checkDigest(self):
        craftDebug.trace("MultiSource checkDigest")
        return self.source.checkDigest()

    def unpack(self):
        craftDebug.trace("MultiSource unpack")
        # pylint: disable=E1101
        # multiple inheritance: MultiSource is never the only
        # superclass, others define self.buildSystemType.
        self.source.buildSystemType = self.buildSystemType
        return self.source.unpack()

    def checkoutDir(self):
        craftDebug.trace("MultiSource checkoutDir")
        return self.source.checkoutDir()

    def sourceDir(self):
        craftDebug.trace("MultiSource sourceDir")
        return self.source.sourceDir()

    def repositoryUrl(self, index=0):
        craftDebug.trace("MultiSource repositoryUrl")
        return self.source.repositoryUrl(index)

    def repositoryUrlCount(self):
        craftDebug.trace("MultiSource repositoryUrlCount")
        return self.source.repositoryUrlCount()

    def applyPatches(self):
        craftDebug.trace("MultiSource applyPatches")
        return self.source.applyPatches()

    def applyPatch(self):
        raise Exception('MultiSource.applyPatch is deprecated. '
                'it calls self.source.applyPatch without arguments which must fail')
        # utils.trace( "MultiSource applyPatch", 2 )
        # return self.source.applyPatch()

    def createPatch(self):
        craftDebug.trace("MultiSource createPatch")
        return self.source.createPatch()

    def getUrls(self):
        craftDebug.trace("MultiSource getUrls")
        return self.source.getUrls()

    def sourceVersion(self):
        craftDebug.trace("MultiSource sourceVersion")
        return self.source.sourceVersion()

    def sourceRevision(self):
        craftDebug.trace("MultiSource sourceVersion")
        return self.source.sourceRevision()


    def printSourceVersion(self):
        craftDebug.trace("MultiSource printSourceVersion")
        print(self.source.sourceVersion())
        return True
