import os
import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ['4.8.1', '4.8.2', '4.8.3', '4.8.4']:
          self.svnTargets[ ver ] = ''

        self.defaultTarget = '4.8.4'


    def setDependencies( self ):
        self.dependencies['kde/kde4-l10n-gl'] = 'default'


from Package.VirtualPackageBase import *
from Packager.PortablePackager import *
class Package( PortablePackager, VirtualPackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        PortablePackager.__init__( self , whitelists = [os.path.join(os.getenv('KDEROOT'),'emerge','portage','package','kde4-l10n-package','whitelist.txt')] )
        VirtualPackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()
