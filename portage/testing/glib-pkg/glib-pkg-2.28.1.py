import os
from shells import MSysShell
import info


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['dev-util/msys'] = 'default'
        self.hardDependencies['dev-util/intltool'] = 'default'
        self.hardDependencies['dev-util/pkg-config'] = 'default'

    def setTargets( self ):
        self.targets[ '2.28.1' ] = 'http://ftp.gnome.org/pub/gnome/sources/glib/2.28/glib-2.28.1.tar.bz2' 
        self.targetInstSrc[ '2.28.1' ] = "glib-2.28.1"  
        self.targetDigests['2.28.1'] = 'f65a89d0a15d0dab07959d01f88502531a4d7ea5'

        
        self.options.package.withCompiler = False

        self.defaultTarget = '2.28.1'

from Package.AutoToolsPackageBase import *

class Package( AutoToolsPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        AutoToolsPackageBase.__init__(self)
        self.shell = MSysShell()
        self.subinfo.options.configure.defines = "--disable-gtk-doc --enable-static=no --enable-shared=yes" 
           
if __name__ == '__main__':
     Package().execute()
