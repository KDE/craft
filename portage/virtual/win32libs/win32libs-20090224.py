from Package.VirtualPackageBase import *
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
win_iconv
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
        self.hardDependencies['virtual/bin-base'] = 'default'
        for package in PACKAGES.split():
            self.hardDependencies['win32libs-bin/' + package] = 'default'
    
class Package( VirtualPackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        VirtualPackageBase.__init__( self )

    def unpack( self ):
        return True

if __name__ == '__main__':
    Package().execute()
