import base
import utils
import os
import shutil
import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.1.0'] = 'http://downloads.sourceforge.net/ebook-tools/ebook-tools-0.1.0.tar.gz'
        self.targetInstSrc['0.1.0'] = 'ebook-tools-0.1.0'
        self.targets['0.1.1'] = 'http://downloads.sourceforge.net/ebook-tools/ebook-tools-0.1.1.tar.gz'
        self.targetInstSrc['0.1.1'] = 'ebook-tools-0.1.1'
        self.defaultTarget = '0.1.1'
    
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['testing/libzip-src'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()
        self.createCombinedPackage = True

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        self.instsrcdir = ""

        # auto-create both import libs with the help of pexports
        self.createImportLibs( "libepub" )

        # now do packaging with kdewin-packager
        self.doPackaging( "ebook-tools", self.buildTarget, True )

        return True
  

if __name__ == '__main__':
    subclass().execute()
