#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
# installing binary packages

from BuildSystem.BuildSystemBase import *

class BinaryBuildSystem(BuildSystemBase):
    def __init__( self):
        BuildSystemBase.__init__(self, "binary")

    def configure( self ):
        return True

    def make( self ):
        return True

    def install( self ):
        if not self.subinfo.targetInstSrc[ self.subinfo.buildTarget ] is None:
            sdir = os.path.join(self.imageDir(),self.subinfo.targetInstSrc[ self.subinfo.buildTarget ] )
            for f in os.listdir(sdir):
                if not utils.moveDir( os.path.join(sdir, f), self.imageDir()):
                    return False

        return BuildSystemBase.install(self)


    def runTest( self ):
        return False
