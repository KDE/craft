import base
import os
import sys
import info
import utils

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/extragear/graphics/digikam'
        for version in ['beta5', 'beta6', 'beta7', 'beta8', 'rc1']:
            self.targets['0.10.0-' + version] = 'http://digikam3rdparty.free.fr/0.10.x-releases/digikam-0.10.0-' + version + '.tar.bz2'
            self.targetInstSrc['0.10.0-' + version] = 'digikam-0.10.0-' + version
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.hardDependencies['kde/kdegraphics'] = 'default'
        self.hardDependencies['win32libs-bin/lcms'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "digikam"
        self.subinfo = subinfo()

    def unpack( self ):
        if self.buildTarget in ['0.10.0-beta5', '0.10.0-beta6', '0.10.0-beta7', '0.10.0-beta8', '0.10.0-rc1']:
            if( not base.baseclass.unpack( self ) ):
                return False
            else:
                return True
        else:
            return self.kdeSvnUnpack()

    def compile( self ):
        self.kdeCustomDefines = "-DENABLE_GPHOTO2=OFF"
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "digikam", self.buildTarget, True )
        else:
            return self.doPackaging( "digikam", os.path.basename(sys.argv[0]).replace("digikam-", "").replace(".py", ""), True )


if __name__ == '__main__':		
    subclass().execute()
