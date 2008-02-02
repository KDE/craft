import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdelibs'
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdelibs'
        self.targets['4.0.60'] = 'ftp://ftp.rz.uni-wuerzburg.de/pub/unix/kde/unstable/4.0.60/src/kdelibs-4.0.60.tar.bz2'
        self.targetInstSrc['4.0.60'] = 'kdelibs-4.0.60'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kdesupport/kdewin32'] = 'default'
        self.hardDependencies['kdesupport/qimageblitz'] = 'default'
        self.hardDependencies['kdesupport/soprano'] = 'default'
        self.hardDependencies['kdesupport/strigi'] = 'default'
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['dev-util/win32libs'] = 'default'
    
class subclass(base.baseclass):
    def __init__(self):
        self.buildType = "Debug"
        base.baseclass.__init__( self, "" )
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        self.kdeCustomDefines = "-DKDE4_BUILD_TESTS=OFF"
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "kdelibs", os.path.basename(sys.argv[0]).replace("kdelibs-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()
