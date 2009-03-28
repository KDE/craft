import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdewebdev'
        self.svnTargets['svnHEAD'] = 'trunk/extragear/multimedia/k3b'
        for ver in ['61', '62', '63', '64']:
          self.targets['4.0.' + ver] = 'ftp://ftp.rz.uni-wuerzburg.de/pub/unix/kde/unstable/4.0.' + ver + '/src/k3b-4.0.' + ver + '.tar.bz2'
          self.targetInstSrc['4.0.' + ver] = 'kdewebdev-4.0.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.hardDependencies['kde/kdemultimedia'] = 'default'
        self.hardDependencies['testing/libsamplerate'] = 'default'
        self.hardDependencies['testing/libdvdcss'] = 'default'
        #        self.hardDependencies['testing/libcdio'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self ):
        base.baseclass.__init__( self, "" )
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "k3b", self.buildTarget, True )
        else:
            return self.doPackaging( "k3b", os.path.basename(sys.argv[0]).replace("k3b-", "").replace(".py", ""), True )


if __name__ == '__main__':
    subclass().execute()
