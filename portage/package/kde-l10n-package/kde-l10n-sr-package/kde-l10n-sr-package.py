import os

import info
import kdedefaults as kd
from EmergeConfig import *


kd.setKDEPath(os.path.join(EmergeStandardDirs.emergeRoot(),'emerge','portage','kde'))

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ['0', '1', '2', '3', '4', '5']:
          self.svnTargets[ kd.kdeversion + ver ] = ''

        self.defaultTarget = kd.kdeversion + '0'


    def setDependencies( self ):
        self.dependencies['kde/kde-l10n-sr'] = 'default'


from Package.VirtualPackageBase import *
from Packager.PortablePackager import *
class Package( PortablePackager, VirtualPackageBase ):
    def __init__( self, **args ):
        PortablePackager.__init__( self , whitelists = [os.path.join(EmergeStandardDirs.emergeRoot(),'emerge','portage','package','kde-l10n-package','whitelist.txt')] )
        VirtualPackageBase.__init__( self )
        self.subinfo.options.package.withArchitecture=False


