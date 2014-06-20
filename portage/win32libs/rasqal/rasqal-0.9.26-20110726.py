import info
import emergePlatform

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['0.9.26', '0.9.30']:
            self.targets[ ver ] = 'http://download.librdf.org/source/rasqal-' + ver + '.tar.gz'
            self.targetInstSrc[ ver ] = 'rasqal-' + ver
        self.patchToApply[ '0.9.26' ] = ( 'rasqal-0.9.26-20130523.diff', 1 )
        self.targetDigests['0.9.26'] = '5496312158c0569bc047b4cab85604a06f116555'
        self.patchToApply[ '0.9.30' ] = ( 'rasqal-0.9.30-20130831.diff', 1 )
        self.targetDigests['0.9.30'] = '8e104acd68fca9b3b97331746e08d53d07d2e20a'
        self.shortDescription = "Rasqal RDF Query Library - for executing RDF queries"
        self.defaultTarget = '0.9.30'

    def setDependencies( self ):
        self.dependencies['win32libs/yajl'] = 'default'
        self.dependencies['win32libs/expat'] = 'default'
        self.dependencies['win32libs/libcurl'] = 'default'
        self.dependencies['win32libs/pcre'] = 'default'
        self.dependencies['win32libs/libxml2'] = 'default'
        self.dependencies['win32libs/libxslt'] = 'default'
        self.dependencies['win32libs/raptor2'] = 'default'        
        self.buildDependencies['virtual/base'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
