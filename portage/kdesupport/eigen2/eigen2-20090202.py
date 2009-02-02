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
        self.svnTargets['2.0-beta5'] = 'tags/eigen/2.0-beta5'
        self.svnTargets['2.0-beta6'] = 'tags/eigen/2.0-beta6'
        self.svnTargets['2.0.0'] = 'tags/eigen/2.0.0'
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/eigen2'
        self.defaultTarget = 'svnHEAD'

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
        if self.traditional:
            self.instdestdir = "kde"
        if self.buildTarget == "svnHEAD":
            return self.doPackaging( "eigen2", utils.cleanPackageName( sys.argv[0], "eigen2" ), True )
        else:
            return self.doPackaging( "eigen2", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()
