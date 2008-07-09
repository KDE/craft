import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdemultimedia'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdelibs'] = 'default'
        self.hardDependencies['kdesupport/phonon'] = 'default'
        self.hardDependencies['kdesupport/taglib'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        self.kdeCustomDefines = "-DBUILD_dragonplayer=OFF"
        self.kdeCustomDefines += " -DBUILD_kscd=OFF"
        self.kdeCustomDefines += " -DBUILD_kcompactdisc=OFF"
#        self.kdeCustomDefines += " -DBUILD_juk=OFF"
        self.kdeCustomDefines += " -DBUILD_strigi-analyzer=OFF"
        self.kdeCustomDefines += " -DBUILD_kioslave=OFF"        # audiocd kioslave
        self.kdeCustomDefines += " -DBUILD_kmix=OFF"
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "kdemultimedia", self.buildTarget, True )
        else:
            return self.doPackaging( "kdemultimedia", os.path.basename(sys.argv[0]).replace("kdepimlibs-", "").replace(".py", ""), True )


if __name__ == '__main__':
    subclass().execute()
