# 
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

import info

from FileSource import *
from ArchiveSource import *
from SvnSource import *
from GitSource import *
from CvsSource import *
from HgSource import *

def SourceFactory(settings):
    """ return sourceBase derived instance for recent settings"""
    utils.debug( "SourceFactory called", 2 )
    source = None
    
    if settings.hasTarget():
        url = settings.target()
        if url.startswith("[archive]"):
            source = ArchiveSource()
        elif url.find(".exe") <> -1 or url.find(".bat") <> -1:
            source = FileSource()
        else:
            source = ArchiveSource()

    ## \todo move settings access into info class 
    if settings.hasSvnTarget():
        url = settings.svnTarget()
        if url.find("://") == -1: 
            source = SvnSource()
        elif url.startswith("[hg]"):
            source = HgSource()
        elif url.find("git:") >= 0 or url.startswith("[git]"):
            source = GitSource()
        elif url.find("svn:") >= 0 or url.find("https:") >= 0 or url.find("http:") >= 0:
            source = SvnSource()
        ## \todo complete more cvs access schemes 
        elif url.find("pserver:") >= 0: 
            source = CvsSource()

    if source == None:
        utils.die("none or unsupported source system set")
        
    source.subinfo = settings
    source.url = url
    return source
