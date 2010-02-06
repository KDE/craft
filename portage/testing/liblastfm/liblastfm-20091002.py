from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['20091002']:
            self.targets[ version ] = 'http://downloads.sourceforge.net/kde-windows/liblastfm-vc90-20091002-bin.tar.bz2'#self.getPackage( repoUrl, "liblastfm", version )

        self.defaultTarget = '20091002'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        self.hardDependencies['testing/libfftw'] = 'default'
        self.hardDependencies['testing/libsamplerate'] = 'default'

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
