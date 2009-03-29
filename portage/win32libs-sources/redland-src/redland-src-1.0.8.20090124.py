import base
import os
import utils
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets[ '1.0.8' ] = 'http://download.librdf.org/source/redland-1.0.8.tar.gz'
        self.targetInstSrc[ '1.0.8' ] = 'redland-1.0.8'
        self.patchToApply[ '1.0.8' ] = ( 'redland-src_1.0.8.patch', 1 )
        self.defaultTarget = "1.0.8"

    def setDependencies( self ):
        self.hardDependencies['testing/sqlite'] = 'default'
        self.hardDependencies['win32libs-bin/libcurl'] = 'default'
        self.hardDependencies['win32libs-bin/libxml2'] = 'default'
        self.hardDependencies['win32libs-bin/libxslt'] = 'default'
        self.hardDependencies['win32libs-bin/openssl'] = 'default'
        self.hardDependencies['win32libs-bin/pcre'] = 'default'


class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, "" )
    self.subinfo = subinfo()

  def compile( self ):
    return self.kdeCompile()

  def install( self ):
    return self.kdeInstall()

  def make_package( self ):
    return self.doPackaging( "redland", self.buildTarget )

if __name__ == '__main__':
    subclass().execute()
