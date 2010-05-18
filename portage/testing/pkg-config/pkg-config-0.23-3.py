from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):      
        arch='32'
        if( os.getenv('EMERGE_ARCHITECTURE')=="x64"):
           arch='64'
        for version in ['0.23-3']: 
            self.targets[ version ] = "http://ftp.gnome.org/pub/gnome/binaries/win"+ arch+"/dependencies/pkg-config_"+version+"_win"+arch+".zip"
        self.targetDigests['0.23-3'] = 'd063e705812e1ee7feb8f35d51b3cad04ca13b0d'
        self.defaultTarget = '0.23-3'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'


class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()