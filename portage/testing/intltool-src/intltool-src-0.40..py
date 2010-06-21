import os
import info


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['dev-util/msys'] = 'default'
        self.hardDependencies['testing/glib'] = 'default'
        self.hardDependencies['testing/pkg-config'] = 'default'

    def setTargets( self ):
        self.targets['0.40.6'] = 'http://ftp.acc.umu.se/pub/gnome/sources/intltool/0.40/intltool-0.40.6.tar.bz2'
        self.targetInstSrc['0.40.6'] = "intltool-0.40.6"
        self.targetDigests['0.40.6'] = '4f6469e09e2c06a8072dffff36f84ff401d7ea75'        

        self.defaultTarget = '0.40.6'

from Package.AutoToolsPackageBase import *

class Package( AutoToolsPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.merge.destinationPath = 'msys'
        self.subinfo.options.package.withCompiler = False
        
if __name__ == '__main__':
     Package().execute()
