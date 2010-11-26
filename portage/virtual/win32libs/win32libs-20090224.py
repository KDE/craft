from Package.VirtualPackageBase import *
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
        self.dependencies['virtual/bin-base'] = 'default'
        for package in PACKAGES.split():
            self.dependencies['win32libs-bin/' + package] = 'default'
    
class Package( VirtualPackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        VirtualPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
