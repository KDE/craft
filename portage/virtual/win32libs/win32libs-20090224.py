import base
import os
import utils
import shutil
import info

PACKAGES= """aspell
libbzip2
expat
gettext
giflib
gpgme
iconv
jasper
jpeg
libpng
libxml2
libxslt
openslp
openssl
redland
shared-mime-info
tiff
zlib
boost
dbus
pcre
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['HEAD'] = ""
        self.defaultTarget = 'HEAD'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        for package in PACKAGES.split():
            self.hardDependencies['win32libs-bin/' + package] = 'default'
    
class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, "" )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
