# -*- coding: utf-8 -*-

import info

from ArchiveSource import *
from SvnSource import *
from KDESvnSource import *
from GitSource import *
from CvsSource import *

def SourceFactory(settings):
    """ return sourceBase derived instance for recent settings"""
    utils.debug( "SourceFactory called", 2 )
    source = None
    
    if settings.hasTarget():
        url = settings.target()
        if utils.verbose > 1:
            print "foung archive target with url=" + url
        source = ArchiveSource()

    ## \todo move settings access into info class 
    if settings.hasSvnTarget():
        url = settings.svnTarget()
        if utils.verbose > 1:
            print "found svn target with url=" + url
        if url.find("://") == -1: 
            if utils.verbose > 1:
                print "found kde svn target with url=" + url
            source = KDESvnSource()
            
        elif url.find("git:") >= 0:
            if utils.verbose > 1:
                print "found git target with url=" + url
            source = GitSource()
         
        elif url.find("svn:") >= 0 or url.find("https:") >= 0 or url.find("http:") >= 0:
            if utils.verbose > 1:
                print "found svn target with url=" + url
            source = SvnSource()

        ## \todo complete more cvs access schemes 
        elif url.find("pserver:") >= 0: 
            if utils.verbose > 1:
                print "found cvs target with url=" + url
            source = CvsSource()

    if source == None:
        utils.die("none or unsupported source system set")
        
    source.subinfo = settings
    source.url = url
    return source
