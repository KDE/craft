# -*- coding: utf-8 -*-

from SourceBase import *
import os

class VersionSystemSourceBase (SourceBase):
    """abstract base class for version system support"""

    noFetch = False

    # host part of svn server 
    kdesvnserver = ""

    # local checkout root path
    kdesvndir = ""
        
    # complete local path for currently used source
    svndir = ""
    
    # from base.py
    DOWNLOADDIR=os.getenv( "DOWNLOADDIR" )
    downloaddir = DOWNLOADDIR
    
    def __init__(self):
        SourceBase.__init__(self)
        
    def checkout(self): abstract
    def update(self): abstract


