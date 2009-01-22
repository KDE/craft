import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.2/kdesdk'
        for ver in ['0']:
          self.targets['4.2.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.2.' + ver + '/src/kdesdk-4.2.' + ver + '.tar.bz2'
          self.targetInstSrc['4.2.' + ver] = 'kdesdk-4.2.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde-4.2/kdebase-runtime'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
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
        return self.doPackaging( "kdesdk", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()
