import base
import utils
import os
import shutil
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        for v in [ '2.7.0' ]:
            self.targets[ v ] = 'http://libarchive.googlecode.com/files/libarchive-' + v + '.tar.gz'
            self.targetInstSrc[ v ] = 'libarchive-' + v
        self.defaultTarget = '2.7.0'
    
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['win32libs-bin/libbzip2'] = 'default'
#        self.hardDependencies['win32libs-bin/lzma'] = 'default'
        self.hardDependencies['win32libs-bin/openssl'] = 'default'
        self.hardDependencies['win32libs-bin/zlib'] = 'default'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        # auto-create both import libs with the help of pexports
        #self.createImportLibs( "libical" )
        #self.createImportLibs( "libicalss" )
        #self.createImportLibs( "libicalvcal" )

        self.doPackaging( "libarchive", self.buildTarget, True )

        return True

if __name__ == '__main__':
    subclass().execute()
