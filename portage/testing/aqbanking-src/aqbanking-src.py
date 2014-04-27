import info
import utils


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.hardDependencies['testing/gwenhywfar-src'] = 'default'
        self.hardDependencies['win32libs/mpir'] = 'default'
        if compiler.isMinGW():
                self.buildDependencies['dev-util/msys'] = 'default'

    def setTargets( self ):
        self.targets['5.0.2'] = 'aqbanking-5.0.2.tar.gz'
        self.targetInstSrc['5.0.2'] = "aqbanking-5.0.2"
        self.targets['5.0.16'] = 'aqbanking-5.0.16.tar.gz'
        self.targetInstSrc['5.0.16'] = "aqbanking-5.0.16"

        self.options.package.withCompiler = False
        self.shortDescription = "Generic Online Banking Interface"
        self.defaultTarget = '5.0.16'

from Package.AutoToolsPackageBase import *
from Package.VirtualPackageBase import *
 
class PackageMinGW(AutoToolsPackageBase):
    def __init__( self, **args ):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.defines = "--enable-shared --disable-static"

    def fetch(self):
        utils.wgetFile('"http://www.aquamaniac.de/sites/download/download.php?package=03&release=87&file=01&dummy=aqbanking-5.0.16.tar.gz"', self.downloadDir() , "aqbanking-5.0.16.tar.gz")
        #utils.wgetFile('"http://www.aquamaniac.de/sites/download/download.php?package=03&release=75&file=01&dummy=aqbanking-5.0.2.tar.gz"' , self.downloadDir() , "aqbanking-5.0.2.tar.gz")
        return True

if compiler.isMinGW():
    class Package(PackageMinGW):
        def __init__( self ):
            PackageMinGW.__init__( self )
else:
    class Package(VirtualPackageBase):
        def __init__( self ):
            VirtualPackageBase.__init__( self )

