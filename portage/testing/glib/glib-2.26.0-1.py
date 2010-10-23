from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):     
        arch='32'
        if( os.getenv('EMERGE_ARCHITECTURE')=="x64"):
           arch='64'
        for version in ['2.24.0-2']:
            self.targets[ version ] = self.getPackageList("http://ftp.acc.umu.se/pub/gnome/binaries/win"+arch+"/glib/2.26/",
                                                          ["glib_2.26.0-1_win"+arch+".zip",
                                                          "glib-dev_2.26.0-1_win"+arch+".zip"])
                                                          
        self.targetDigests['2.24.0-2'] = ['4a2b4effeba93a9fdb5f591c856845c328239efa',
                                          'f54e9766e19a007e21535dc2a28c16babc827865']

        self.defaultTarget = '2.24.0-2'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
    