import info
import emergePlatform
import compiler

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['0.9.26']:
            self.targets[ ver ] = 'http://download.librdf.org/source/rasqal-' + ver + '.tar.gz'
            self.targetInstSrc[ ver ] = 'rasqal-' + ver
        self.patchToApply[ '0.9.26' ] = ( 'rasqal-0.9.26-20110726.diff', 1 )
        self.targetDigests['0.9.26'] = '5496312158c0569bc047b4cab85604a06f116555'
        self.shortDescription = "Rasqal RDF Query Library - for executing RDF queries"
        self.defaultTarget = '0.9.26'

    def setDependencies( self ):
        self.dependencies['win32libs-bin/yajl'] = 'default'
        self.dependencies['win32libs-bin/expat'] = 'default'
        self.dependencies['win32libs-bin/libcurl'] = 'default'
        self.dependencies['win32libs-bin/pcre'] = 'default'
        self.dependencies['win32libs-bin/libxml2'] = 'default'
        self.dependencies['win32libs-bin/libxslt'] = 'default'
        self.dependencies['win32libs-bin/raptor2'] = 'default'        
        self.buildDependencies['virtual/base'] = 'default'
        if compiler.isMinGW():
            self.dependencies['win32libs-bin/mpir'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
