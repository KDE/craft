import base
import os
import utils
import shutil
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.7.3-1'] = "http://fontconfig.org/release/fontconfig-2.7.3.tar.gz"
        self.targets['2.8.0-1'] = "http://fontconfig.org/release/fontconfig-2.8.0.tar.gz"
        self.patchToApply['2.7.3-1'] = ('fontconfig-2.7.3.diff', 1)
        self.patchToApply['2.8.0-1'] = ('fontconfig-2.8.0.diff', 1)
        self.targetInstSrc['2.7.3-1'] = "fontconfig-2.7.3"
        self.targetInstSrc['2.8.0-1'] = "fontconfig-2.8.0"
        self.defaultTarget = '2.8.0-1'
    
    def setDependencies( self ):
        self.hardDependencies['kdesupport/kdewin'] = 'default'
        self.hardDependencies['win32libs-sources/freetype-src'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.createCombinedPackage = False
        self.subinfo = subinfo()

    def kdeSvnPath( self ):
        return False
    
    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        self.doPackaging( "fontconfig", self.buildTarget, True )

        return True

if __name__ == '__main__':
    subclass().execute()
