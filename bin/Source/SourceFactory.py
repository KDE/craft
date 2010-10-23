# 
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

import info
import utils

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
        type = utils.getVCSType( settings.svnTarget() )
        if type == "svn":
            source = SvnSource()
        elif type == "hg":
            source = HgSource()
        elif "git":
            source = GitSource()
        ## \todo complete more cvs access schemes 
        elif "cvs": 
            source = CvsSource()

    if source == None:
        utils.die("none or unsupported source system set")
        
    source.subinfo = settings
    source.url = url
    return source
