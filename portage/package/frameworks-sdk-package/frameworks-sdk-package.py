import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ['0.1']:
          self.svnTargets[ ver ] = ''

        self.defaultTarget = '0.1'


    def setDependencies( self ):
        self.dependencies['dev-util/frameworks-sdk'] = 'default'
        self.dependencies['dev-util/emerge'] = 'default'
        self.dependencies['frameworks/kcoreaddons'] = 'default'
        #self.dependencies['frameworks/tier2'] = 'default'
        #self.dependencies['frameworks/tier3'] = 'default'
        #self.dependencies['frameworks/tier4'] = 'default'


from Package.VirtualPackageBase import *
from Packager.SevenZipPackager import *

class Package( SevenZipPackager, VirtualPackageBase ):
    def __init__( self, **args ):
        VirtualPackageBase.__init__( self )
        SevenZipPackager.__init__( self )
        #self.subinfo.options.package.packageName = "test"


