import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdeedu'
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdeedu'
        for ver in ['66', '67', '70']:
          self.targets['4.0.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.0.' + ver + '/src/kdeedu-4.0.' + ver + '.tar.bz2'
          self.targetInstSrc['4.0.' + ver] = 'kdeedu-4.0.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'

        self.softDependencies['kdesupport/eigen'] = 'default'
        self.softDependencies['kdesupport/gmm'] = 'default'
        self.softDependencies['win32libs-sources/cfitsio-src'] = 'default'
        self.softDependencies['win32libs-sources/libnova-src'] = 'default'
        self.softDependencies['win32libs-sources/openbabel-src'] = 'default'
    
class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
        self.instsrcdir = "kdeedu"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        self.kdeCustomDefines = "-DBUILD_doc=OFF"
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "kdeedu", self.buildTarget, True )
        else:
            return self.doPackaging( "kdeedu", os.path.basename(sys.argv[0]).replace("kdeedu-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()
