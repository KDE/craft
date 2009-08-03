import base
import utils
from utils import die
import sys
import info

# see http://eigen.tuxfamily.org/ for more informations

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        self.targets['2.0.4'] = "http://bitbucket.org/eigen/eigen2/get/2.0.4.tar.bz2"
        self.targetInstSrc['2.0.4'] = "eigen2"
        self.defaultTarget = '2.0.4'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        # header-only package
        self.createCombinedPackage = True
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        self.kdeCustomDefines = "-DBUILD_TESTS=OFF"
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if self.buildTarget == "svnHEAD":
            return self.doPackaging( "eigen2" )
        else:
            return self.doPackaging( "eigen2", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()
