from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):      
        arch='32'
        if( os.getenv('EMERGE_ARCHITECTURE')=="x64"):
           arch='64'
        for version in ['0.23-2']: 
            self.targets[ version ] = "http://ftp.gnome.org/pub/gnome/binaries/win"+ arch+"/dependencies/pkg-config_0.23-2_win"+arch+".zip"

        self.defaultTarget = '0.23-2'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'


class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()