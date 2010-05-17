import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        self.targets['4.2'] = 'http://www.docbook.org/xml/4.2/docbook-xml-4.2.zip'
		self.targetDigests['4.2'] = '5e3a35663cd028c5c5fbb959c3858fec2d7f8b9e'		
        self.defaultTarget = '4.2'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__( self )
        self.subinfo.options.install.installPath = 'share/xml/docbook/schema/dtd/4.2'

if __name__ == '__main__':
    Package().execute()
