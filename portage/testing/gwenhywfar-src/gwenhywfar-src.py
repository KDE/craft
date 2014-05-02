import info
import utils


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['testing/gnutls-src'] = 'default'
        if compiler.isMinGW():
                self.buildDependencies['dev-util/msys'] = 'default'

    def setTargets( self ):
        self.targets['4.0.3'] = 'gwenhywfar-4.0.3.tar.gz'
        self.targetInstSrc['4.0.3'] = "gwenhywfar-4.0.3"       
        self.patchToApply['4.0.3'] = ('gwenhywfar-4.0.3-20110122.diff', 1)
        self.targets['4.3.0'] = 'gwenhywfar-4.3.0.tar.gz'
        self.targetInstSrc['4.3.0'] = "gwenhywfar-4.3.0"       
        self.patchToApply['4.3.0'] = ('gwenhywfar-4.0.3-20110122.diff', 1)

        self.options.package.withCompiler = False
        self.shortDescription = "A multi-platform helper library for other libraries"
        self.defaultTarget = '4.0.3'

from Package.AutoToolsPackageBase import *
from Package.VirtualPackageBase import *
 
class PackageMinGW(AutoToolsPackageBase):
    def __init__( self, **args ):
        AutoToolsPackageBase.__init__(self)
        mergeroot = self.shell.toNativePath( self.mergeDestinationDir() )
        self.subinfo.options.configure.defines = "--enable-shared --disable-static --with-guis=qt4 --with-qt4-includes=" + mergeroot + "/include --with-qt4-libs=" + mergeroot + "/lib --with-qt4-moc=" + mergeroot + "/bin/moc.exe --with-qt4-uic=" + mergeroot + "/bin/uic.exe"

    def fetch(self):
        utils.wgetFile('"http://www.aquamaniac.de/sites/download/download.php?package=01&release=56&file=01&dummy=gwenhywfar-4.0.3.tar.gz"' , SourceBase.downloadDir() , "gwenhywfar-4.0.3.tar.gz")
        return True

if compiler.isMinGW():
    class Package(PackageMinGW):
        def __init__( self ):
            PackageMinGW.__init__( self )
else:
    class Package(VirtualPackageBase):
        def __init__( self ):
            VirtualPackageBase.__init__( self )

