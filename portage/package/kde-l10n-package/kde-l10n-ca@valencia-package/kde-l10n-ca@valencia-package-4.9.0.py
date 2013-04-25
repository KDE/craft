import os
import info
import kdedefaults as kd

kd.setKDEPath(os.path.join(os.getenv('KDEROOT'),'emerge','portage','kde'))

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ['0', '1', '2', '3', '4', '5']:
          self.svnTargets[ kd.kdeversion + ver ] = ''

        self.defaultTarget = kd.kdeversion + '0'


    def setDependencies( self ):
        self.dependencies['kde/kde-l10n-ca@valencia'] = 'default'


from Package.VirtualPackageBase import *
from Packager.PortablePackager import *
class Package( PortablePackager, VirtualPackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        PortablePackager.__init__( self , whitelists = [os.path.join(os.getenv('KDEROOT'),'emerge','portage','package','kde-l10n-package','whitelist.txt')] )
        VirtualPackageBase.__init__( self )
        self.subinfo.options.package.withArchitecture=False


if __name__ == '__main__':
    Package().execute()
