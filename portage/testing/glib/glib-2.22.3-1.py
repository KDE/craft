from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):        
        for version in ['2.22.3-1']:
            self.targets[ version ] = """http://ftp.gnome.org/pub/gnome/binaries/win32/glib/2.22/glib_2.22.3-1_win32.zip
			                          """+"""http://ftp.gnome.org/pub/gnome/binaries/win32/glib/2.22/glib-dev_2.22.3-1_win32.zip"""

        self.defaultTarget = '2.22.3-1'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()