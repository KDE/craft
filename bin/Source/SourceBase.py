# -*- coding: utf-8 -*-

from EmergeBase import *

class SourceBase(EmergeBase):
    """ implements basic stuff required for all sources"""
    def __init__(self):
        EmergeBase.__init__(self)
        self.url = ""

    def fetch(self): 
        """fetch the source from a remote host and save it into a local destination"""
        abstract()

    def unpack(self): 
        """unpack the source into a local destination."""
        abstract()
        
    def sourceDir(self): 
        """return local source dir""" 
        abstract()

    def applyPatches(self):
        """apply patches is available"""
        utils.debug( "SourceBase.applyPatches called", 1 )

        if self.subinfo.hasTarget():
            ( file, patchdepth ) = self.subinfo.patchesToApply()
            if file:
                patchfile = os.path.join ( self.packagedir, file )
                srcdir = os.path.join ( self.workDir(), self.instsrcdir )
                return utils.applyPatch( patchfile, srcdir, patchdepth )
        return True

