import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdeedu'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
    
class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
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
#        self.kdeCustomDefines += " -DBUILD_marble=OFF"
        self.kdeCustomDefines += " -DBUILD_step=OFF"
        self.kdeCustomDefines += " -DBUILD_keduvocdocument=OFF"
        self.kdeCustomDefines += " -DBUILD_kdeeduui=OFF"
        self.kdeCustomDefines += " -DBUILD_libscience=OFF"
        
        self.kdeCustomDefines += " -DTILES_AT_COMPILETIME=OFF"
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "marble-kde", self.buildTarget, True )
        else:
            return self.doPackaging( "marble-kde", os.path.basename(sys.argv[0]).replace("marble-kde-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()
