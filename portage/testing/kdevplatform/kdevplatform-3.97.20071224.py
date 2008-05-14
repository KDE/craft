import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdevplatform'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdelibs'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self, **args ):
        self.buildType="Debug"
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "kdevplatform"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "kdevplatform", os.path.basename(sys.argv[0]).replace("kdevplatform-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()
