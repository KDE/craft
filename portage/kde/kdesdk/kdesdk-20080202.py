import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdesdk'
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdesdk'
        self.targets['4.0.60'] = 'ftp://ftp.rz.uni-wuerzburg.de/pub/unix/kde/unstable/4.0.60/src/kdesdk-4.0.60.tar.bz2'
        self.targetInstSrc['4.0.60'] = 'kdesdk-4.0.60'
        self.targets['4.0.61'] = 'ftp://ftp.rz.uni-wuerzburg.de/pub/unix/kde/unstable/4.0.61/src/kdesdk-4.0.61.tar.bz2'
        self.targetInstSrc['4.0.61'] = 'kdesdk-4.0.61'
        self.targets['4.0.62'] = 'ftp://ftp.rz.uni-wuerzburg.de/pub/unix/kde/unstable/4.0.62/src/kdesdk-4.0.62.tar.bz2'
        self.targetInstSrc['4.0.62'] = 'kdesdk-4.0.62'
        self.targets['4.0.63'] = 'ftp://ftp.rz.uni-wuerzburg.de/pub/unix/kde/unstable/4.0.63/src/kdesdk-4.0.63.tar.bz2'
        self.targetInstSrc['4.0.63'] = 'kdesdk-4.0.63'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        
class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
        self.subinfo = subinfo()
        self.kdeCustomDefines = ""
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kate=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kapptemplate=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kbugbuster=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kcachegrind=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kdeaccounts-plugin=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kdepalettes=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_strigi-analyzer=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kioslave=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kmtrace=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kprofilemethod=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kuiviewer=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_poxml=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_scripts=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_umbrello=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_doc=OFF "
        

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "kdesdk", self.buildTarget, True )
        else:
            return self.doPackaging( "kdesdk", os.path.basename(sys.argv[0]).replace("kdesdk-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()
