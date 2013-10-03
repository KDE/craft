import info

class subinfo( info.infoclass ):

    def setTargets( self ):
        for ver in [ '3.1.1' ]:
            self.targets[ ver ] = 'http://www.apache.org/dist/xerces/c/3/sources/xerces-c-' + ver + '.tar.gz'
            self.targetInstSrc[ ver ] = 'xerces-c-' + ver
        self.targetDigests['3.1.1'] = '177ec838c5119df57ec77eddec9a29f7e754c8b2'

        self.shortDescription = "A Validating XML Parser"
        self.defaultTarget = '3.1.1'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

from Package.AutoToolsPackageBase import *

class Package(AutoToolsPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        AutoToolsPackageBase.__init__(self)

        self.buildInSource=True

if __name__ == '__main__':
      Package().execute()

