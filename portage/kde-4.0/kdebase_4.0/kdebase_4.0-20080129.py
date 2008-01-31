import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdebase'
        self.svnTargets['4.0.1'] = 'tags/KDE/4.0.1/kdebase'
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.0/kdebase'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde-4.0/kdelibs_4.0'] = 'default'
        self.hardDependencies['kde-4.0/kdepimlibs_4.0'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self ):
        base.baseclass.__init__( self, "" )
        self.instsrcdir = "kdebase"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "kdebase", os.path.basename(sys.argv[0]).replace("kdebase_4.0-", "").replace(".py", ""), True )

		
if __name__ == '__main__':
    subclass().execute()
