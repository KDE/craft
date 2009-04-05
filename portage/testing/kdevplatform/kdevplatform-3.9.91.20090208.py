import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdevplatform'
        self.svnTargets['0.9.92'] = 'tags/kdevplatform/0.9.92'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self, **args ):
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
        if self.buildTarget == "svnHEAD":
            return self.doPackaging( "kdevplatform", os.path.basename(sys.argv[0]).replace("kdevplatform-", "").replace(".py", ""), True )
        else:
            return self.doPackaging( "kdevplatform", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()
