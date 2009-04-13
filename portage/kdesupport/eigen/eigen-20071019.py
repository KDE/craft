import base
import utils
from utils import die
import sys
import info

# http://download.tuxfamily.org/eigen/eigen-1.0.5.tar.gz
# see http://eigen.tuxfamily.org/ for more informations

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        self.targets['1.0.5'] = 'http://download.tuxfamily.org/eigen/eigen-1.0.5.tar.gz'
        self.targetInstSrc['1.0.5'] = "eigen"
        self.defaultTarget = '1.0.5'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        # header-only package
        self.createCombinedPackage = True
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if self.buildTarget == "svnHEAD":
            return self.doPackaging( "eigen" )
        else:
            return self.doPackaging( "eigen", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()
