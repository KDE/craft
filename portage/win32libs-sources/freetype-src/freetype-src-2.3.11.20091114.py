import base
import os
import utils
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.3.7-2'] = "http://downloads.sourceforge.net/freetype/freetype-2.3.7.tar.bz2"
        self.targets['2.3.11-1'] = "http://downloads.sourceforge.net/freetype/freetype-2.3.11.tar.bz2"
        self.patchToApply['2.3.7-2'] = ('freetype.diff', 1)
        self.patchToApply['2.3.11-1'] = ('freetype-2.3.11.diff', 1)
        self.targetInstSrc['2.3.7-2'] = "freetype-2.3.7"
        self.targetInstSrc['2.3.11-1'] = "freetype-2.3.11"
        self.defaultTarget = '2.3.11-1'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.createCombinedPackage = False
        self.subinfo = subinfo()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        self.doPackaging( "freetype", self.buildTarget, True )

        return True

if __name__ == '__main__':
    subclass().execute()
