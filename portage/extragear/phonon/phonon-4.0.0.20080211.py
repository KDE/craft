import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kdereview'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdelibs'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self ):
        base.baseclass.__init__( self, "" )
        self.instsrcdir = "phonon"
        self.kdeCustomDefines = "-DBUILD_binary-clock=OFF -DBUILD_fuzzy-clock=OFF -DBUILD_ksystemlog=OFF -DBUILD_kollision=OFF"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "phonon", os.path.basename(sys.argv[0]).replace("phonon-", "").replace(".py", ""), True )

if __name__ == '__main__':		
    subclass().execute()
