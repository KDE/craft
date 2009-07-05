# -*- coding: utf-8 -*-

import info

from ArchiveSource import *
from SvnSource import *
from KDESvnSource import *
from GitSource import *
from CvsSource import *

def SourceFactory(settings):
    """ return sourceBase derived instance for recent settings"""
    utils.debug( "SourceFactory called", 1 )
    
    if settings.hasTarget():
        url = settings.target()
        if utils.verbose > 1:
            print "foung archive target with url=" + url
        source = ArchiveSource()
        source.url = url
        return source

    # todo move settings access into info class 
    if settings.hasSvnTarget():
        url = settings.svnTarget()
        if url.find("://") == -1: 
            if utils.verbose > 1:
                print "foung kde svn target with url=" + url
            source = KDESvnSource()
            source.url = url
            return source
            
        if url.find("git:"):
            if utils.verbose > 1:
                print "foung git svn target with url=" + url
            source = GitSource()
            source.url = url
            return source
         
        if url.find("svn:") or url.find("https:") or url.find("http:"):
            if utils.verbose > 1:
                print "foung git svn target with url=" + url
            source = SvnSource()
            source.url = url
            return source

        # todo complete more cvs access schemes 
        if url.find("pserver:"): 
            if utils.verbose > 1:
                print "foung cvs target with url=" + url
            source = CvsSource()
            source.url = url
            return source
    return None
