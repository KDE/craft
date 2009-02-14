import base
import os
import sys
import info
import utils

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/extragear/graphics/kipi-plugins'
        self.svnTargets['branch-0.3'] = 'branches/extragear/graphics/kipi-plugins'
        for version in ['beta3', 'beta4', 'beta5', 'beta6', 'rc1', 'rc2']:
            self.targets['0.2.0-' + version] = 'http://digikam3rdparty.free.fr/0.10.x-releases/kipi-plugins-0.2.0-' + version + '.tar.bz2'
            self.targetInstSrc['0.2.0-' + version] = 'kipi-plugins-0.2.0-' + version
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.hardDependencies['kde/kdegraphics'] = 'default'
        self.hardDependencies['win32libs-bin/gettext'] = 'default'
        self.hardDependencies['dev-util/gettext-tools'] = 'default'
        self.hardDependencies['win32libs-bin/expat'] = 'default'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "digikam"
        self.subinfo = subinfo()

    def unpack( self ):
        if self.buildTarget in ['0.2.0-beta3', '0.2.0-beta4', '0.2.0-beta5', '0.2.0-beta6', '0-2.0-rc1', '0.2.0-rc2']:
            if( not base.baseclass.unpack( self ) ):
                return True
            else:
                return False
        else:
            return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "kipi-plugins", self.buildTarget, True )
        else:
            return self.doPackaging( "kipi-plugins", os.path.basename(sys.argv[0]).replace("kipi-plugins-", "").replace(".py", ""), True )


if __name__ == '__main__':		
    subclass().execute()
