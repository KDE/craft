import base
import os
import shutil
import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        self.targets['3.0'] = 'http://download.gna.org/getfem/stable/gmm-3.0.tar.gz'
        self.targetInstSrc['3.0'] = 'gmm-3.0'
        self.defaultTarget = '3.0'

class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
        # header-only package
        self.createCombinedPackage = True
        self.subinfo = subinfo()

    def unpack( self ):
        if not self.kdeSvnUnpack():
            return False
        src = os.path.join( self.packagedir , "CMakeLists.txt" )
        dst = os.path.join( self.workdir, self.instsrcdir, "CMakeLists.txt" )
        shutil.copy( src, dst )
        return True

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( 'gmm', self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()
