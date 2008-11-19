import base
import os
import utils
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/playground/edu'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "rocs"
        self.subinfo = subinfo()
        
    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        self.kdeCustomDefines = ""
        self.kdeCustomDefines += " -DBUILD_kard=OFF"
        self.kdeCustomDefines += " -DBUILD_kalcul=OFF"
        self.kdeCustomDefines += " -DBUILD_keduca=OFF"
        self.kdeCustomDefines += " -DBUILD_kurriculum=OFF"
        self.kdeCustomDefines += " -DBUILD_physiks=OFF"
        self.kdeCustomDefines += " -DBUILD_kverbos=OFF"
        self.kdeCustomDefines += " -DBUILD_kiddraw=OFF"
        self.kdeCustomDefines += " -DBUILD_doc=OFF"
#        self.kdeCustomDefines += " -DBUILD_Rocs=OFF"
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "Rocs", "20081119", True )
		
if __name__ == '__main__':
    subclass().execute()
