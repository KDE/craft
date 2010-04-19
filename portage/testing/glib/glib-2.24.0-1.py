from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):     
        arch='32'
        if( os.getenv('EMERGE_ARCHITECTURE')=="x64"):
           arch='64'
        for version in ['2.24']:
            self.targets[ version ] = self.getPackageList("ftp.gnome.org/pub/gnome/binaries/win"+arch+"/glib/2.24",
                                                          ["glib_2.24.0-1_win"+arch+".zip",
                                                          "glib-dev_2.24.0-1_win"+arch+".zip"])
        self.targetDigests['2.24'] = ['11c52267d9ae06f507a3eee66ae25e35c89b8c77',
                                      '45bd47470d10e691d29f0e3a9ce1371a0d38f149']                                                          
   
        self.defaultTarget = '2.24'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
    