import os
import info


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['dev-util/msys'] = 'default'

    def setTargets( self ):
        self.targets['2.2.8'] = 'http://ftp.gnu.org/gnu/libtool/libtool-2.2.8.tar.lzma'
        self.targetDigests['2.2.8'] = 'e160056cab3b0d31db6c929f12ddd4a77e2a024d'
        self.targetInstSrc['2.2.8'] = "libtool-2.2.8"

        self.defaultTarget = '2.2.8'

from Package.AutoToolsPackageBase import *

class Package( AutoToolsPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.merge.destinationPath = 'msys'
        self.subinfo.options.package.withCompiler = False
        
if __name__ == '__main__':
     Package().execute()
