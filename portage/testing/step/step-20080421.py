import base
import os
import utils
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kde/kdeedu'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "kdeedu"
        self.subinfo = subinfo()
        
    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        self.kdeCustomDefines = ""
        self.kdeCustomDefines += " -DBUILD_blinken=OFF"
        self.kdeCustomDefines += " -DBUILD_doc=OFF"
        self.kdeCustomDefines += " -DBUILD_kalzium=OFF"
        self.kdeCustomDefines += " -DBUILD_kalgebra=OFF"
        self.kdeCustomDefines += " -DBUILD_kanagram=OFF"
        self.kdeCustomDefines += " -DBUILD_kbruch=OFF"
        self.kdeCustomDefines += " -DBUILD_kgeography=OFF"
        self.kdeCustomDefines += " -DBUILD_khangman=OFF"
        self.kdeCustomDefines += " -DBUILD_kig=OFF"
        self.kdeCustomDefines += " -DBUILD_kiten=OFF"
        self.kdeCustomDefines += " -DBUILD_klettres=OFF"
        self.kdeCustomDefines += " -DBUILD_kmplot=OFF"
        self.kdeCustomDefines += " -DBUILD_kpercentage=OFF"
        self.kdeCustomDefines += " -DBUILD_kstars=OFF"
        self.kdeCustomDefines += " -DBUILD_ktouch=OFF"
        self.kdeCustomDefines += " -DBUILD_kturtle=OFF"
        self.kdeCustomDefines += " -DBUILD_parley=OFF"
        self.kdeCustomDefines += " -DBUILD_kwordquiz=OFF"
        self.kdeCustomDefines += " -DBUILD_marble=OFF"
#        self.kdeCustomDefines += " -DBUILD_step=OFF"
        self.kdeCustomDefines += " -DBUILD_keduvocdocument=OFF"
#        self.kdeCustomDefines += " -DBUILD_kdeeduui=OFF"
#        self.kdeCustomDefines += " -DBUILD_libscience=OFF"
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "step", "20080311", True )
		
if __name__ == '__main__':
    subclass().execute()
