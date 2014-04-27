import os

import info


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        for ver in ['1.75.2', '1.78.0', '1.78.1']:
            self.targets[ ver ] = 'http://downloads.sourceforge.net/docbook/docbook-xsl-' + ver + '.tar.bz2'
        self.targetDigests['1.75.2'] = 'cd146012c07f3c2c79c1cd927ad1faf5bee6cc74'
        self.targetDigests['1.78.0'] = '39a62791e7c1479e22d13d12a9ecbb2273d66229'
        self.targetDigests['1.78.1'] = '1d668c845bb43c65115d1a1d9542f623801cfb6f'
        self.options.package.withCompiler = False
        self.options.package.packSources = False

        self.shortDescription = "document translation defintions for docbook format"
        self.defaultTarget = '1.78.1'


    def setDependencies( self ):
        self.dependencies['data/docbook-dtd'] = '4.5' # actually, all v4 should work

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self ):
        BinaryPackageBase.__init__( self )

    def unpack( self ):
        """rename the directory here"""
        self.subinfo.options.install.installPath = 'share/xml/docbook'
        if not BinaryPackageBase.unpack(self):
            return False
        os.rename(os.path.join(self.installDir(), os.path.basename(self.repositoryUrl()).replace(".tar.bz2", "")),
                  os.path.join(self.installDir(), "xsl-stylesheets-" + self.subinfo.buildTarget))
        self.subinfo.options.install.installPath = ''
        utils.copyFile(os.path.join(self.packageDir(), "docbook-xsl-stylesheets-1.78.1.xml"), os.path.join(self.installDir(), "etc", "xml", "docbook-xsl-stylesheets.xml"))
        return True

if __name__ == '__main__':
    Package().execute()
