#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
import CraftDebug
import utils

from Source.ArchiveSource import *
from Source.SvnSource import *
from Source.GitSource import *
from Source.HgSource import *

def SourceFactory(settings):
    """ return sourceBase derived instance for recent settings"""
    CraftDebug.trace("SourceFactory called", 1)
    source = None

    if settings.hasTarget():
        if settings.hasMultipleTargets():
            url = settings.targetAt(0)
        else:
            url = settings.target()
        source = ArchiveSource(settings)

    ## \todo move settings access into info class
    if settings.hasSvnTarget():
        url = settings.svnTarget()
        sourceType = utils.getVCSType( url )
        if sourceType == "svn":
            source = SvnSource(settings)
        elif sourceType == "hg":
            source = HgSource(settings)
        elif sourceType == "git":
            source = GitSource(settings)

    if source == None:
        CraftDebug.die("none or unsupported source system set")
    if not source.subinfo:
        source.subinfo = settings
    source.url = url
    return source
