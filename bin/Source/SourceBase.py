# 
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

from EmergeBase import *

class SourceBase(EmergeBase):
    """ implements basic stuff required for all sources"""
    def __init__(self):
        utils.debug( "SourceBase.__init__ called", 2 )
        EmergeBase.__init__(self)
        self.url = ""

    def fetch(self): 
        """fetch the source from a remote host and save it into a local destination"""
        abstract()

    def unpack(self): 
        """unpack the source into a local destination."""
        abstract()
        
    def sourceDir(self): 
        sourcedir = self.workDir()
        if hasattr(self, 'buildSystemType') and self.buildSystemType == 'binary':
            sourcedir = self.imageDir()

        if self.subinfo.hasTargetSourcePath():
            sourcedir = os.path.join(sourcedir, self.subinfo.targetSourcePath())
        if utils.verbose > 1:
            print "using sourcedir: " + sourcedir
        return sourcedir

    def applyPatches(self):
        """apply patches is available"""
        utils.debug( "SourceBase.applyPatches called", 2 )

        if self.subinfo.hasTarget():
            ( file, patchdepth ) = self.subinfo.patchesToApply()
            if file:
                patchfile = os.path.join ( self.packageDir(), file )
                srcdir = os.path.join ( self.sourceDir() )
                return utils.applyPatch( patchfile, srcdir, patchdepth )
        return True

