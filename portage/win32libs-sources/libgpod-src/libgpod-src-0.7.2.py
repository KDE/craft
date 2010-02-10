import os
from shells import MSysShell
import info


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['dev-util/msys'] = 'default'
        self.hardDependencies['testing/glib'] = 'default'
        self.hardDependencies['testing/pkg-config'] = 'default'
        self.hardDependencies['win32libs-bin/sqllite'] = 'default'
        self.hardDependencies['testing/libplist-src'] = 'default'
        self.hardDependencies['testing/intltool-src'] = 'default'

    def setTargets( self ):
        self.targets['0.7.2'] = 'http://kent.dl.sourceforge.net/project/gtkpod/libgpod/libgpod-0.7.2/libgpod-0.7.2.tar.gz'
        self.targetInstSrc['0.7.2'] = "libgpod-0.7.2"
        self.patchToApply['0.7.2'] = ("libgpod-0.7.2.diff", 1)        
        
        self.targets['0.7.90'] = 'http://www.gnome.org/~teuf/libgpod-0.7.90GIT.tar.gz'
        self.targetInstSrc['0.7.90'] = "libgpod-0.7.90GIT"
        
        self.options.package.withCompiler = False

        self.defaultTarget = '0.7.2'

from Package.PackageBase import *
from Source.MultiSource import *
from BuildSystem.AutoToolsBuildSystem import *
from Packager.KDEWinPackager import *;

class Package( PackageBase, MultiSource, AutoToolsBuildSystem, KDEWinPackager):
    def __init__( self ):
        self.subinfo = subinfo()
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        AutoToolsBuildSystem.__init__(self)
        KDEWinPackager.__init__(self)
        self.subinfo.options.configure.defines = """--with-python=no --disable-static LIBXML_CFLAGS=-I""" + \
        MSysShell().toNativePath( os.path.join( self.rootdir, "include", "libxml" ) ) + """ LIBXML_LIBS=-lxml2"""
           
if __name__ == '__main__':
     Package().execute()
