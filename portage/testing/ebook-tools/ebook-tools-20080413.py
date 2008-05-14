import base
import utils
import os
import shutil
import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.1.0'] = 'http://downloads.sourceforge.net/ebook-tools/ebook-tools-0.1.0.tar.gz'
        self.targetInstSrc['0.1.0'] = 'ebook-tools-0.1.0'
        self.defaultTarget = '0.1.0'
    
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['testing/libzip-src'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

if __name__ == '__main__':
    subclass().execute()
