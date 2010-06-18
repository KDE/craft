import os
from shells import MSysShell
import info


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['dev-util/msys'] = 'default'

    def setTargets( self ):
        self.targets['2.2.8'] = 'http://ftp.gnu.org/gnu/libtool/libtool-2.2.8.tar.gz'
        self.targetInstSrc['2.2.8'] = "libtool-2.2.8"
        self.targetDigests['2.2.8'] = 'e0fd6f9d39c81c2da8b548411c74a46c24442abf'
        self.options.package.withCompiler = False
        
        self.targetMergePath['2.2.8']= "msys";

        self.defaultTarget = '2.2.8'

from Package.AutoToolsPackageBase import *

class Package( AutoToolsPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        AutoToolsPackageBase.__init__(self)
        self.buildInSource = True
        
if __name__ == '__main__':
     Package().execute()
