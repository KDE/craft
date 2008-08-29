import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.1/kdegames'
        for ver in ['0', '1']:
          self.targets['4.1.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.1.' + ver + '/src/kdegames-4.1.' + ver + '.tar.bz2'
          self.targetInstSrc['4.1.' + ver] = 'kdegames-4.1.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde-4.1/kdebase-runtime'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()

    def unpack( self ):
        self.kdeSvnUnpack()
        return True

    def compile( self ):
        self.kdeCustomDefines = ""
#        self.kdeCustomDefines += " -DBUILD_doc=OFF"
#        self.kdeCustomDefines += " -DBUILD_bovo=OFF"
#        self.kdeCustomDefines += " -DBUILD_lskat=OFF"
#        self.kdeCustomDefines += " -DBUILD_katomic=OFF"
#        self.kdeCustomDefines += " -DBUILD_kbattleship=OFF"
#        self.kdeCustomDefines += " -DBUILD_kblackbox=OFF"
#        self.kdeCustomDefines += " -DBUILD_kblocks=OFF"
#        self.kdeCustomDefines += " -DBUILD_kbounce=OFF"
#        self.kdeCustomDefines += " -DBUILD_kbreakout=OFF"
#        self.kdeCustomDefines += " -DBUILD_kdiamond=OFF"
#        self.kdeCustomDefines += " -DBUILD_kfourinline=OFF"
#        self.kdeCustomDefines += " -DBUILD_kgoldrunner=OFF"
#        self.kdeCustomDefines += " -DBUILD_kiriki=OFF"
#        self.kdeCustomDefines += " -DBUILD_kjumpingcube=OFF"
#        self.kdeCustomDefines += " -DBUILD_klines=OFF"
#        self.kdeCustomDefines += " -DBUILD_kmahjongg=OFF"
#        self.kdeCustomDefines += " -DBUILD_kmines=OFF"
#        self.kdeCustomDefines += " -DBUILD_knetwalk=OFF"
#        self.kdeCustomDefines += " -DBUILD_kolf=OFF"
#        self.kdeCustomDefines += " -DBUILD_kollision=OFF"
#        self.kdeCustomDefines += " -DBUILD_konquest=OFF"
#        self.kdeCustomDefines += " -DBUILD_kpat=OFF"
#        self.kdeCustomDefines += " -DBUILD_kreversi=OFF"
#        self.kdeCustomDefines += " -DBUILD_ksame=OFF"
#        self.kdeCustomDefines += " -DBUILD_kshisen=OFF"
#        self.kdeCustomDefines += " -DBUILD_ksirk=OFF"
#        self.kdeCustomDefines += " -DBUILD_kspaceduel=OFF"
#        self.kdeCustomDefines += " -DBUILD_ksquares=OFF"
#        self.kdeCustomDefines += " -DBUILD_ktuberling=OFF"
#        self.kdeCustomDefines += " -DBUILD_ksudoku=OFF"
#        self.kdeCustomDefines += " -DBUILD_kubrick=OFF"
        return self.kdeCompile()
    
    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "kdegames", self.buildTarget, True )
        else:
            return self.doPackaging( "kdegames", os.path.basename(sys.argv[0]).replace("kdegames-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()
