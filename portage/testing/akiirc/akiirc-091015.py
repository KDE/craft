import base
import utils
import os
import sys
import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/playground/network/akiirc'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdelibs'] = 'default'
        self.hardDependencies['win32libs-bin/openssl'] = 'default'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()
        
    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "akiirc", self.buildTarget, True )
        else:
            return self.doPackaging( "akiirc", os.path.basename(sys.argv[0]).replace("akiirc-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()
