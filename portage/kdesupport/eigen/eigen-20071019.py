import base
import utils
from utils import die
import os
import sys
import info

# http://download.tuxfamily.org/eigen/eigen-1.0.5.tar.gz
# see http://eigen.tuxfamily.org/ for more informations
class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

    def setTargets( self ):
#        self.targets['1.0.5'] = 'http://download.tuxfamily.org/eigen/eigen-1.0.5.tar.gz'
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/eigen'
        self.defaultTarget = 'svnHEAD'

class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
        # header-only package
        self.createCombinedPackage = True
        self.instsrcdir = "eigen"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if self.traditional:
            self.instdestdir = "kde"
        return self.doPackaging( "eigen", os.path.basename(sys.argv[0]).replace("eigen-", "").replace(".py", ""), True )        

if __name__ == '__main__':
    subclass().execute()
