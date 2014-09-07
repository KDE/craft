import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ['0.3']:
          self.svnTargets[ ver ] = ''

        self.defaultTarget = '0.3'


    def setDependencies( self ):
        self.dependencies['qt-libs/snorenotify'] = 'default'


from Package.VirtualPackageBase import *
from Packager.PortablePackager import *
class Package( PortablePackager, VirtualPackageBase ):
    def __init__( self, **args ):
        whitelists = [ 'whitelist.txt' ]
        VirtualPackageBase.__init__( self )
        PortablePackager.__init__( self , whitelists)
        


