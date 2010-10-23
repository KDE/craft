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
        self.targetDigests['2.24.0-2'] = ['0efd5f86f526bc3ec63eebe1b31709918708f0d6',
                                          'b41715b4c1379a0172c47a8b54b3208ece20f14e']   
        self.defaultTarget = '2.24.0-2'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
    