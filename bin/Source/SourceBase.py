# -*- coding: utf-8 -*-

from EmergeBase import *

class SourceBase(EmergeBase):
    """ implements basic stuff required for  all sources"""
    url = ""
    def __init__(self):
        EmergeBase.__init__(self)

    def fetch(self): abstract()

    def unpack(self): abstract()

    def sourceDir(self): abstract()

    def applyPatches(self):
        """ apply patches is available """
        utils.debug( "SourceBase.__applyPatches called", 1 )

        if self.subinfo.hasTarget():
            ( file, patchdepth ) = self.subinfo.patchesToApply()
            patchfile = os.path.join ( self.packagedir, file )
            srcdir = os.path.join ( self.workdir, self.instsrcdir )
            return utils.applyPatch( patchfile, srcdir, patchdepth )
        return True

