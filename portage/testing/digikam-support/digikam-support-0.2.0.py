import base
import utils
import shutil
import os
import sys
import info

class subinfo (info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        self.targets['0.1.0'] = "http://saroengels.net/kde-windows/gnuwin32/digikam-support-0.1.0.tar.bz2"
        self.targetInstSrc['0.1.0'] = "digikam-support"
        self.targets['0.2.0'] = "http://saroengels.net/kde-windows/gnuwin32/digikam-support-0.2.0.tar.bz2"
        self.targetInstSrc['0.2.0'] = "digikam-support-0.2.0"
        self.defaultTarget = '0.2.0'


class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()

    def unpack( self ):
        if( not base.baseclass.unpack( self ) ):
            return False
        return True

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "digikam-support", self.buildTarget, True )

    
if __name__ == '__main__':
    subclass().execute()
