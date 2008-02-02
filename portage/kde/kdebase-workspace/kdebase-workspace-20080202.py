import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdebase/workspace'
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdebase/workspace'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdelibs'] = 'default'
        self.hardDependencies['kde/kdepimlibs'] = 'default'
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self ):
        base.baseclass.__init__( self, "" )
        self.instsrcdir = "workspace"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "kdebase-workspace", os.path.basename(sys.argv[0]).replace("kdebase-workspace-", "").replace(".py", ""), True )

		
if __name__ == '__main__':
    subclass().execute()
