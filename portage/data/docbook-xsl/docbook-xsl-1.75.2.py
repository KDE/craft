import info
import shutil
import os

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        self.targets['1.75.2'] = 'http://downloads.sourceforge.net/docbook/docbook-xsl-1.75.2.tar.bz2'
        self.targetDigests['1.75.2'] = 'cd146012c07f3c2c79c1cd927ad1faf5bee6cc74'
        self.defaultTarget = '1.75.2'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__( self )
        self.subinfo.options.install.installPath = 'share/xml/docbook'
        
    def unpack( self ):
        """rename the directory here"""
        if not BinaryPackageBase.unpack(self):
            return False
        os.rename(os.path.join(self.installDir(), os.path.basename(self.repositoryUrl()).replace(".tar.bz2", "")), 
                  os.path.join(self.installDir(), "xsl-stylesheets-" + self.subinfo.buildTarget))
        return True

if __name__ == '__main__':
    Package().execute()
